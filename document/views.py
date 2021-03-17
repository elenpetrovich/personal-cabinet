import re
from rest_framework import serializers, viewsets, mixins, views, status, exceptions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from bson import ObjectId
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from rest_framework import permissions
from django.core.files.storage import default_storage
from django.views.static import serve
from django.core.exceptions import PermissionDenied

from .models import db_docs, DocumentFile
from cabinet.models import Account, Company
from mysite.settings import MONGODB_KEY
from cabinet.serializers import CompanySerializer, AccountSerializer
from .serializer import DocumentFileSerializers, FileUploadSerializers


class DocumentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_collection(self):
        self.get_company()
        self.collection = self.company.mongodb_collection
        if not bool(self.collection):
            raise exceptions.NotFound("Коллекция не найдена")

    def get_company(self):
        self.company = Company.objects.filter(
            name=self.request.query_params.get("company", ""),
            users=self.request.user,
        ).first()
        if self.company is None:
            raise exceptions.NotFound("Компания не найдена")

    def get_doc_file(self, mongodb_id):
        return DocumentFile.objects.filter(
            company=self.company,
            mongodb_id=mongodb_id,
        ).first()

    def list(self, request):
        self.get_collection()
        search = {}
        for query in request.query_params:
            if query[0] == "_":
                search.update({query[1:]: str(request.query_params[query])})
        data = db_docs[self.collection].find(search)
        serializer = CompanySerializer(self.company)
        return Response(
            {
                "document_list": list(data),
                "company": serializer.data
            },
            template_name="document_list.html",
        )

    def retrieve(self, request, pk=None):
        self.get_collection()
        data = db_docs[self.collection].find_one({"_id": ObjectId(pk)})
        if data is None:
            raise exceptions.NotFound("Документ не найден")
        if request.query_params.get("no_company", "0") == "1":
            return Response({"document": data})
        serializer = CompanySerializer(self.company)
        return Response(
            {
                "document": data,
                "company": serializer.data
            },
            template_name="document_detail.html",
        )

    @action(detail=True, methods=['get'], url_path="print")
    def print(self, request, pk=None):
        self.get_collection()
        data = db_docs[self.collection].find_one({"_id": ObjectId(pk)})
        if data is None:
            raise exceptions.NotFound("Документ не найден")
        doc_file = self.get_doc_file(str(data["_id"]))
        if doc_file is None:
            file_request = DocumentFile(
                mongodb_id=str(data["_id"]),
                company=self.company,
            )
            doc_file = file_request.save()
        company_serializer = CompanySerializer(self.company)
        file_serializer = DocumentFileSerializers(doc_file)
        return Response(
            {
                "document": data,
                "company": company_serializer.data,
                "file": file_serializer.data,
                "first_request": bool(doc_file),
            },
            template_name="document_print.html",
        )


class ByHeaderKey(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if MONGODB_KEY == request.headers.get("API-KEY", ""):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class SyncViewSet(viewsets.ViewSet):
    permission_classes = [ByHeaderKey]

    def get_collection(self, company_name, secret_key):
        company = self.get_company(company_name, secret_key)
        if company is not None:
            collection = company.mongodb_collection
            if bool(collection) is True:
                return collection
        return None

    def get_company(self, company_name, secret_key):
        company = Company.objects.filter(name=company_name).first()
        if company and company.secret_key:
            if company.secret_key != secret_key:
                return None
        return company

    def get_hash(self, value):
        return make_password(value)

    def list(self, request):
        return Response({})

    @action(detail=False,
            methods=['get', 'post'],
            url_path="docs",
            url_name="docs")
    def sync_docs(self, request):
        if request.method in permissions.SAFE_METHODS:
            return Response({})
        data = {}
        for number, company in enumerate(request.data.keys()):
            collection = self.get_collection(
                company, request.headers.get("COMPANY-" + str(number + 1), ""))
            if collection is not None:
                data[company] = []
                for doc in request.data[company]:
                    new_doc = self.save_doc(doc, collection)
                    data[company].append(new_doc)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=['get', 'post'],
            url_path="users",
            url_name="users")
    def sync_users(self, request, *args, **kwargs):
        if request.method in permissions.SAFE_METHODS:
            return Response({})
        data = {}
        for number, company in enumerate(request.data.keys()):
            company_data = self.get_company(
                company, request.headers.get("COMPANY-" + str(number + 1), ""))
            if company_data is not None:
                data[company] = []
                for user in request.data[company]:
                    new_user = self.save_user(user, company_data)
                    data[company].append(new_user)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=['get', 'post'],
            url_path="company",
            url_name="company")
    def sync_company(self, request, *args, **kwargs):
        if request.method in permissions.SAFE_METHODS:
            return Response({})
        data = {}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=['get', 'post'],
            url_path="file_request",
            url_name="file_request")
    def sync_file_request(self, request, *args, **kwargs):
        if request.method in permissions.SAFE_METHODS:
            return Response({})
        data = {}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False,
            methods=['get', 'post'],
            url_path="file",
            url_name="file")
    def sync_file(self, request, *args, **kwargs):
        if request.method in permissions.SAFE_METHODS:
            return Response({})
        serializer = FileUploadSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_data = self.get_company(serializer.data["company"],
                                        request.headers.get("COMPANY-1", ""))
        if company_data is None:
            raise exceptions.NotFound("Компания не найдена")
        data = serializer.validated_data
        reg = re.compile('[^a-zA-ZА-я0-9_ ]')
        file_name = f"{reg.sub('', data['company'])}/{reg.sub('', data['file_rule']).lower()}/{data['file_ref']}.{data['file_format']}"
        file_path = default_storage.save(
            file_name,
            data["file_data"],
        )
        file_url = default_storage.url(file_name)
        return Response(
            {
                "url": file_url,
                "file_name": file_name
            },
            status=status.HTTP_201_CREATED,
        )

    def save_doc(self, doc: dict, collection: str, pk: str = "Ref"):
        result = db_docs[collection].replace_one({pk: doc[pk]}, doc, True)
        return doc[pk], result.modified_count, str(result.upserted_id)

    def save_user(self, user: dict, company: str):
        db_user = Account.objects.filter(username=user["username"]).first()
        serializer = AccountSerializer(instance=db_user, data=user)
        password = None
        if serializer.is_valid(raise_exception=False):
            new_user: Account = serializer.save()
            if db_user is None:
                password = get_random_string(8)
                new_user.password = make_password(password)
                new_user.save()
                # new_user.groups.add(group, group, ...)
        return user["username"], bool(db_user), password

    def save_company(self, company: dict):
        return ""


category_name = {
    "all": ["all", "все", "общий"],
    "user": ["private", "сотрудники", "приватный"],
}


def serve_with_permissions(request,
                           path,
                           document_root=None,
                           show_indexes=False):
    if request.user.is_authenticated:
        path_parts = path.split("/")
        if len(path_parts) == 3:  # company/category/file.name
            if path_parts[1] in category_name["all"]:
                pass
            elif path_parts[1] in category_name["user"]:
                company = Company.objects.filter(name=path_parts[0],
                                                 users=request.user).first()
                if company is None:
                    raise PermissionDenied
            else:
                company = Company.objects.filter(name=path_parts[0],
                                                 users=request.user).first()
                if company is None:
                    raise PermissionDenied
                print(path_parts[2])
        return serve(request, path, document_root, show_indexes)
    raise PermissionDenied