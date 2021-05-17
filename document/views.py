from pymongo import collection
from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from bson import ObjectId
from rest_framework import permissions
from django.views.static import serve
from django.core.exceptions import PermissionDenied

from .models import Document, client
from company.models import Company, Collection
from company.serializers import CompanySerializer, CollectionSerializer

attributes = {
    "link": "link",
    "secret": "secret",
    "data": "data",
}  #TODO: или в бд добавить правило для коллекции


class DocumentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    collection_pk = "collection_pk"
    company_pk = "company_pk"

    def get_exclude_doc_list(self):
        doc_perm = Document.objects.exclude(
            roles__users=self.request.user).values_list('id').all()
        return [ObjectId(x[0]) for x in list(doc_perm)]

    def is_allowed_doc(self, mongodb_id):
        doc_perm = Document.objects.filter(id=mongodb_id).first()
        if doc_perm is None:
            raise exceptions.PermissionDenied("Документ не доступен")
        # elif doc_perm.public is False and Collection.objects.filter(
        #         id=doc_perm.collection.id,
        #         roles__users=self.request.user).first() is None:
        #     raise exceptions.PermissionDenied("Документ не доступен")

    def get_collection(self, **kwargs):
        self.get_company(**kwargs)
        self.collection = Collection.objects.filter(
            company=self.company,
            public_name=kwargs.get("collection_pk", ""),
            roles__users=self.request.user).first()
        if self.collection is None:
            raise exceptions.NotFound("Коллекция не найдена")

    def get_company(self, **kwargs):
        self.company = self.request.user.get_companies(
            kwargs.get(self.company_pk, "")).first()
        if self.company is None:
            raise exceptions.NotFound("Компания не найдена")

    def get_doc_files(self, mongodb_id: str, collection_id: int):
        # return DocumentFile.objects.filter(id=mongodb_id).first()
        return None

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
        for key in keys: # "link0_Поставщик" - ссылка; "Поставщик" - значение
            parts = key.split("0_")
            if parts[0] == attributes["link"]:
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
                    doc[f'{attributes["data"]}.{link[1]}'] = self.extend_links(
                        self.get_mongodb(collection).find_one({"Ref": doc[link[0]]}),
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
        search.update({"_id": {"$nin": self.get_exclude_doc_list()}})
        data = []
        for doc in self.get_mongodb().find(search):
            data.append(self.extend_links(doc, depth_max=1))
        return Response(
            {"document_list": data} | self.get_subdata(),
            template_name="document_list.html",
        )

    def retrieve(self, request, pk=None, **kwargs):
        self.get_collection(**kwargs)
        self.is_allowed_doc(pk)
        data = self.get_mongodb().find_one({"_id": ObjectId(pk)})
        if data is None:
            raise exceptions.NotFound("Документ не найден")
        return Response(
            {
                "document": data,
            } | self.get_subdata(),
            template_name="document_detail.html",
        )

    @action(detail=True, methods=['get'], url_path="print")
    def print(self, request, pk=None, **kwargs):
        self.get_collection(**kwargs)
        self.is_allowed_doc(pk)
        data = self.get_mongodb().find_one({"_id": ObjectId(pk)})
        if data is None:
            raise exceptions.NotFound("Документ не найден")
        doc_file = self.get_doc_file(pk)
        # if doc_file:
        #     file_request = DocumentFile(id=pk,
        #                                 ref=data["Ref"],
        #                                 collection=self.collection)
        #     doc_file = file_request.save()
        # file_serializer = DocumentFileSerializers(doc_file)
        file_serializer = None
        file_request = None
        return Response(
            {
                "document": data,
                "file": file_serializer.data,
                "first_request": bool(file_request)
            } | self.get_subdata(),
            template_name="document_print.html",
        )


class FileRender():
    category_name = {
        "all": ["all", "все", "общий"],
        "user": ["private", "сотрудники", "приватный"],
    }

    @classmethod
    def serve_with_permissions(cls,
                               request,
                               path,
                               document_root=None,
                               show_indexes=False):
        if request.user.is_authenticated:
            path_parts = path.split("/")
            if len(path_parts) == 3:  # company/category/file.name
                if path_parts[1] in cls.category_name["all"]:
                    pass
                elif path_parts[1] in cls.category_name["user"]:
                    company = Company.objects.filter(
                        name=path_parts[0], users=request.user).first()
                    if company is None:
                        raise PermissionDenied
                else:
                    company = Company.objects.filter(
                        name=path_parts[0], users=request.user).first()
                    if company is None:
                        raise PermissionDenied
                    print(path_parts[2])
            return serve(request, path, document_root, show_indexes)
        raise PermissionDenied