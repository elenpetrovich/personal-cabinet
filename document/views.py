from pathlib import Path
import posixpath
from datetime import datetime

from django.views.static import serve
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.utils._os import safe_join
from django.conf import settings
from django.shortcuts import redirect

from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from bson import ObjectId

from .models import Document, client, RequestDoc
from .serializer import RequestDocSerializer
from company.models import Company, Collection
from company.serializers import CompanySerializer, CollectionSerializer


class DocumentMixin():
    def get_allowed_doc_list(self):
        doc_perm = Document.objects.filter(
            collection=self.collection,
            roles__users=self.request.user).values_list('id').all()
        return [ObjectId(x[0]) for x in list(doc_perm)]

    def is_allowed_doc(self, mongodb_id) -> Document:
        document_config = Document.objects.filter(id=mongodb_id).annotate(
            roles_user_count=Count(
                "roles",
                filter=Q(roles__users=self.request.user),
            ),
            roles_count=Count("roles"),
        ).first()
        if document_config is None:
            raise exceptions.PermissionDenied("Документ не доступен")
        elif document_config.is_public is False and document_config.roles_user_count == 0:
            raise exceptions.PermissionDenied("Документ не доступен")
        return document_config

    def get_collection(self, **kwargs):
        self.get_company(**kwargs)
        self.collection = Collection.objects.filter(
            company=self.company,
            url_name=kwargs.get("collection_pk", ""),
            roles__users=self.request.user).first()
        if self.collection is None:
            raise exceptions.NotFound("Коллекция не найдена")

    def get_company(self, **kwargs):
        self.company = self.request.user.get_companies(
            kwargs.get("company_pk", "")).first()
        if self.company is None:
            raise exceptions.NotFound("Компания не найдена")


class DocumentViewSet(viewsets.ViewSet, DocumentMixin):
    permission_classes = [permissions.IsAuthenticated]

    def get_mongodb(self, collection: str = None):
        if collection is None:
            return client.get_database(self.company.mongo_db).get_collection(
                self.collection.mongo_collection)
        else:
            return client.get_database(self.company.mongo_db).get_collection(
                collection.mongo_collection)

    def get_subdata(self) -> dict:
        return {
            "company": CompanySerializer(self.company).data,
            "collection": CollectionSerializer(self.collection).data
        }

    def find_links(self, keys: list) -> list:
        result = []
        for key in keys:  # "link0_Поставщик" - ссылка; "Поставщик" - значение
            parts = key.split("0_")
            if parts[0] == "link":
                result.append([key, parts[1]])
        return result

    def extend_links(self,
                     doc: dict,
                     depth: int = 0,
                     depth_max: int = 0) -> dict:
        if depth >= depth_max or doc is None:
            return doc
        else:
            depth += 1
            for link in self.find_links(doc.keys()):
                collection = Collection.objects.filter(
                    link_name=link[1]).first()
                if collection is not None:
                    doc[f'data.{link[1]}'] = self.extend_links(
                        self.get_mongodb(collection).find_one(
                            {"Ref": doc[link[0]]}),
                        depth=depth,
                        depth_max=depth_max,
                    )
            return doc

    def list(self, request, **kwargs):
        self.get_collection(**kwargs)
        search = {}
        for query in request.query_params:
            if query[0] == "_":
                search.update({query[1:]: str(request.query_params[query])})
        search.update({"_id": {"$in": self.get_allowed_doc_list()}})
        data = []
        for doc in self.get_mongodb().find(search):
            data.append(self.extend_links(doc, depth_max=1))
        return Response(
            {"document_list": data} | self.get_subdata(),
            template_name="document_list.html",
        )

    def retrieve(self, request, pk=None, **kwargs):
        self.get_collection(**kwargs)
        config = self.is_allowed_doc(pk)
        data = self.get_mongodb().find_one({"_id": ObjectId(pk)})
        if data is None:
            raise exceptions.NotFound("Документ не найден")
        return Response(
            {"document": data} | self.get_subdata(),
            template_name="document_detail.html",
        )

    @action(detail=True, methods=['get'], url_path="print")
    def print(self, request, pk=None, **kwargs):
        self.get_collection(**kwargs)
        config = self.is_allowed_doc(pk)
        file_list = []
        fullpath = config.folder
        for f in fullpath.iterdir():
            if not f.name.startswith('.'):
                file_list.append((str(f.relative_to(fullpath)),
                                  datetime.fromtimestamp(f.stat().st_mtime)))
        file_list.sort(key=lambda x: x[1])
        if len(file_list) == 0:
            file_request, first_request = RequestDoc.objects.get_or_create(
                document_id=pk, kind=1, text="ffr", user=request.user)
        else:
            file_request = None
            first_request = False
        return Response(
            {
                "document_id": config.id,
                "file_request": file_request,
                "first_request": first_request,
                "file_list": file_list,
            } | self.get_subdata(),
            template_name="document_print.html",
        )


class DocumentRequestViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RequestDoc.objects
    serializer_class = RequestDocSerializer

    def is_allowed_doc(self, mongodb_id) -> Document:
        document_config = Document.objects.filter(id=mongodb_id).annotate(
            roles_user_count=Count(
                "roles",
                filter=Q(roles__users=self.request.user),
            ),
            roles_count=Count("roles"),
        ).first()
        if document_config is None:
            raise exceptions.PermissionDenied("Документ не доступен")
        elif document_config.is_public is False and document_config.roles_user_count == 0:
            raise exceptions.PermissionDenied("Документ не доступен")
        return document_config

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user,
            document=self.is_allowed_doc(self.kwargs.get("document_pk")),
        ).all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "request_list": serializer.data,
            } | kwargs,
            template_name="document_requests.html",
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"request": serializer.data} | kwargs,
            template_name="document_requests.html",
        )

    def create(self, request, *args, **kwargs):
        try:
            serializer = RequestDocSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                user=request.user,
                document=self.is_allowed_doc(self.kwargs.get("document_pk")),
            )
            print(kwargs)
            return redirect('requests-detail',
                            pk=serializer.data.get("id"),
                            **kwargs)
        except Exception as e:
            print(e)
            return Response(
                {'error': str(e)} | kwargs,
                template_name="document_requests.html",
            )


class FileRender():
    @classmethod
    def is_allowed_doc(cls, user, mongodb_id) -> Document:
        document_config = Document.objects.filter(id=mongodb_id).annotate(
            roles_user_count=Count(
                "roles",
                filter=Q(roles__users=user),
            ),
            roles_count=Count("roles"),
        ).first()
        if document_config is None:
            raise exceptions.PermissionDenied("Нет доступа к файлу")
        elif document_config.is_public is False and document_config.roles_user_count == 0:
            raise exceptions.PermissionDenied("Нет доступа к файлу")
        return document_config

    @classmethod
    def serve_with_permissions(
        cls,
        request,
        path,
        document_root=None,
        show_indexes=False,
    ):
        if request.user.is_authenticated:
            return serve(request, path, document_root, show_indexes)
        else:
            raise PermissionDenied

    @classmethod
    def serve_document_folder(cls,
                              request,
                              document_root=None,
                              show_indexes=None,
                              **kwargs):
        if request.user.is_authenticated:
            config = cls.is_allowed_doc(request.user,
                                        kwargs.get("document_pk"))
            return serve(
                request,
                f"{config.file_folder}/{kwargs.get('file_name')}",
                document_root,
                show_indexes=True,
            )
        raise PermissionDenied("Нет доступа к файлу")