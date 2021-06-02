import re
from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

from django.core.files.storage import default_storage
from django.utils import timezone
from bson import ObjectId

from mysite.settings import X_API_KEY
from company.models import Company, Collection, Role
from document.models import RequestDoc, Document, client
from cabinet.models import Account, AccountController
from .serializers import FileUploadSerializers, RoleUploadSerializer, UserUploadSerializer, CompanyUploadSerializer, CollectionUploadSerializer, DocListUploadSerializer, RequestDocUploadSerializer


class ByHeaderKeyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if X_API_KEY == request.headers.get("X-API-KEY", ""):
            return True
        return bool(request.user and request.user.is_staff)
        # return False


class SyncViewMixin(viewsets.ViewSet):
    permission_classes = [ByHeaderKeyOrAdmin]

    def get_collection(self, url_name):
        if self.company is not None:
            return Collection.objects.filter(company=self.company,
                                             url_name=url_name).first()
        raise exceptions.NotFound("Коллекция не найдена")

    def get_company(self):
        self.company = Company.objects.filter(
            system_name=self.request.headers.get("X-COMPANY-SYS", "")).first()
        if self.company is None:
            raise exceptions.PermissionDenied("Компания не доступна")
        if not self.verify_key(self.company.secret_key,
                               self.request.headers.get("X-COMPANY-KEY", "")):
            raise exceptions.PermissionDenied("Компания не доступна")

    def verify_key(self, company_key: str, input_key: str):
        return company_key == input_key

    def save_or_edit(self, data):
        return data


class SyncCompanyViewSet(SyncViewMixin):
    def create(self, request, *args, **kwargs):
        self.get_company()
        serializer = CompanyUploadSerializer(self.company,
                                             data=request.data,
                                             partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SyncUserViewSet(SyncViewMixin):
    def create(self, request, *args, **kwargs):
        self.get_company()
        try:
            return Response(self.save_or_edit(request.data))
        except Exception as e:
            raise exceptions.APIException(e)

    def save_or_edit(self, data):
        user = Account.objects.filter(
            controller__user__username=data.get("username")).first()
        new_password = get_random_string(8)
        if user is None:
            serializer = UserUploadSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save(
                username=
                f'{data.get("username")}_{self.company.id}_{get_random_string(3)}',
                password=make_password(new_password),
            )
            AccountController(user=user, company_creator=self.company).save()
        else:
            serializer = UserUploadSerializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return dict(serializer.data) | {"password": new_password}


class SyncCollectionViewSet(SyncViewMixin):
    def create(self, request, *args, **kwargs):
        self.get_company()
        try:
            return Response(self.save_or_edit(request.data))
        except Exception as e:
            raise exceptions.APIException(e)

    def save_or_edit(self, data):
        collection = Collection.objects.filter(
            company=self.company, url_name=data.get("url_name")).first()
        if collection is None:
            serializer = CollectionUploadSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                company=self.company,
                mongo_collection=
                f'{serializer.validated_data.get("url_name")}_{get_random_string("4")}'
            )
        else:
            serializer = CollectionUploadSerializer(collection,
                                                    data=data,
                                                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return serializer.data


class SyncRoleViewSet(SyncViewMixin):
    def create(self, request, *args, **kwargs):
        self.get_company()
        try:
            return Response(self.save_or_edit(request.data))
        except Exception as e:
            raise exceptions.APIException(e)

    def save_or_edit(self, data):
        serializer = RoleUploadSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        role = Role.objects.get_or_create(name=data.get("name"),
                                          company=self.company)
        if data.get("delete_old_collections", False):
            role.collections_set.clear()
        if data.get("delete_old_users", False):
            role.users_set.clear()
        for url_name in data.get("collections_list", []):
            role.collections.add(
                Collection.objects.filter(company=self.company,
                                          url_name=url_name).first())
        for username in data.get("username_list", []):
            role.users.add(
                Account.objects.filter(controller__company=self.company,
                                       username=username).first())
        return serializer


class SyncDocsViewSet(SyncViewMixin):
    def create(self, request):
        self.get_company()
        self.collection = self.get_collection(request.data.get("url_name", ""))
        try:
            return Response(self.save_or_edit_list(request.data))
        except Exception as e:
            raise exceptions.APIException(e)

    def save_or_edit_list(self, data):
        serializer = DocListUploadSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        result = {}
        if serializer.validated_data.get("delete_old", False):
            client.get_database(self.company.mongo_db).get_collection(
                self.collection.mongo_collection).delete_many({})
        roles = Role.objects.filter(
            company=self.company,
            name__in=serializer.validated_data.get("role_list", []),
        ).all()
        for number, doc in enumerate(serializer.validated_data.get("docs",
                                                                   [])):
            sub_result, doc = self.save_or_edit(doc)
            if doc is not None:
                for role in roles:
                    doc.roles.add(role)
            result[number] = {
                "is_new": bool(sub_result.upserted_id),
                "new_id": doc.upserted_id,
            }
        return result

    def save_or_edit(self, data):
        ref = data.get("Ref")
        doc = None
        result = client.get_database(self.company.mongo_db).get_collection(
            self.collection.mongo_collection).replace_one({"Ref": ref}, data,
                                                          True)
        if result.upserted_id:
            doc = Document(id=str(result.upserted_id),
                           ref=ref,
                           collection=self.collection,
                           file_folder=None)
            doc.folder = None
            doc.save()
        return result, doc


class SyncDocsFileViewSet(SyncViewMixin):
    def create(self, request, *args, **kwargs):
        self.get_company()
        serializer = FileUploadSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_path = self.save_or_edit(serializer.validated_data)
        return Response({"file_path": file_path})

    def save_or_edit(self, data):
        doc = Document.objects.filter(
            ref=data.get("ref"), collection__company=self.company).first()
        if doc is not None:
            name = data["file_data"].name
            if data.get("file_name"):
                name = data.get("file_name")
            print(name)
            file_path = default_storage.save(
                f"{str(doc.folder)}/{name}",
                data["file_data"],
            )
        return file_path


class SyncDocsRequestsViewSet(SyncViewMixin):
    def list(self, request, *args, **kwargs):
        self.get_company()
        queryset = RequestDoc.objects.filter(
            document__collection__company=self.company,
            kind=request.query_params.get("kind", 0)).all()
        serializer = RequestDocUploadSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.get_company()
        instance = RequestDoc.objects.filter(
            id=kwargs.get("pk"),
            document__collection__company=self.company).first()
        if not instance:
            raise exceptions.NotFound("Заявка не найдена")
        serializer = RequestDocUploadSerializer(instance,
                                                data=request.data,
                                                partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
