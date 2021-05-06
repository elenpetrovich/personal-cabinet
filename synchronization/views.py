from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from mysite.settings import X_API_KEY
from company.models import Company, Collection
from .serializers import FileUploadSerializers, RoleUploadSerializer, UserUploadSerializer, CompanyUploadSerializer, CollectionUploadSerializer, DocListUploadSerializer, FileRequestSerializers
from .savers import save_doc, save_role, save_file, save_collection, get_file_request, save_user


class ByHeaderKeyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if X_API_KEY == request.headers.get("X-API-KEY", ""):
            return True
        return bool(request.user and request.user.is_staff)
        # return False


class SyncViewSet(viewsets.ViewSet):
    permission_classes = [ByHeaderKeyOrAdmin]

    def get_collection(self, collection_name):
        if self.company is not None:
            return Collection.objects.filter(company=self.company,
                                             name=collection_name).first()
        return None

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

    def list(self, request):
        return Response({})

    @action(detail=False, methods=['post'], url_path="docs", url_name="docs")
    def sync_docs(self, request):
        self.get_company()
        data = {}
        serializer = DocListUploadSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        for number, upload in enumerate(serializer.validated_data):
            collection = save_collection(
                upload["name"],
                self.company,
                link_name=upload.get("link_name"),
            )
            data[f"{number}_{upload['name']}"] = []
            for doc in upload["docs"]:
                new_doc = save_doc(doc, self.company, collection)
                data[f"{number}_{upload['name']}"].append(new_doc)
        return Response(data)

    @action(detail=False, methods=['post'], url_path="users", url_name="users")
    def sync_users(self, request, *args, **kwargs):
        self.get_company()
        data = {}
        serializer = UserUploadSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        for number, user in enumerate(serializer.validated_data):
            new_user = save_user(user, self.company)
            data[str(number)].append(new_user)
        return Response(data)

    @action(detail=False, methods=['post'], url_path="roles", url_name="roles")
    def sync_roles(self, request, *args, **kwargs):
        self.get_company()
        data = {}
        serializer = RoleUploadSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        for number, upload in enumerate(serializer.validated_data):
            role = save_role(upload, self.company)
            data[f"{number}_{upload['name']}"].append(role)
        return Response(data)

    @action(detail=False,
            methods=['post'],
            url_path="company",
            url_name="company")
    def sync_company(self, request, *args, **kwargs):
        self.get_company()
        serializer = CompanyUploadSerializer(self.company,
                                             data=request.data,
                                             partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path="file", url_name="file")
    def sync_file(self, request, *args, **kwargs):
        self.get_company()
        serializer = FileUploadSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_path, file_url, request = save_file(serializer.validated_data,
                                                 self.company)
        return Response({"url": file_url, "file_name": file_path})

    @action(detail=False,
            methods=['get'],
            url_path="file_request",
            url_name="file_request")
    def sync_file_request(self, request, *args, **kwargs):
        self.get_company()
        serializer = FileRequestSerializers(get_file_request(self.company),
                                            many=True)
        return Response(data=serializer.data)

    @action(detail=False,
            methods=['get'],
            url_path="docs_request",
            url_name="docs_request")
    def sync_docs_request(self, request, *args, **kwargs):
        self.get_company()
        return Response(data={})