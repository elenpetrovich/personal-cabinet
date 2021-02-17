from django.contrib.auth.models import User
from pymongo import collection
from rest_framework import serializers, viewsets, mixins, views, status, exceptions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from copy import copy
from bson import ObjectId
from .models import db_docs


class DocumentViewSet(viewsets.ViewSet):
    default_type = "test-1c"

    def get_collection(self, query):
        collection = query.get("type")
        if not collection:
            return self.default_type
            raise exceptions.NotFound("Коллекция не найдена")
        return collection

    def list(self, request):
        collection = self.get_collection(request.query_params)
        search = {}
        for query in request.query_params:
            if query[0] == "_":
                search.update({query[1:]: str(request.query_params[query])})
        data = db_docs[collection].find(search)
        return Response(list(data))

    def retrieve(self, request, pk=None):
        collection = self.get_collection(request.query_params)
        data = db_docs[collection].find_one({"_id": ObjectId(pk)})
        if data is None:
            raise exceptions.NotFound("Документ не найден")
        return Response(data)

    def create(self, request):
        collection = self.get_collection(request.query_params)
        if not request.data:
            raise exceptions.NotFound("Данные не найдены")
        data = db_docs[collection].insert_one(request.data).inserted_id
        return Response({"_id": str(data)})

    # def update(self, request, pk=None):
    #     collection = self.get_collection(request.query_params)
    #     data = db_docs[collection].find_one_and_update({"_id": ObjectId(pk)},
    #                                                 request.data)
    #     return Response(data)

    def destroy(self, request, pk=None):
        collection = self.get_collection(request.query_params)
        data = db_docs[collection].delete_one({
            "_id": ObjectId(pk)
        }).deleted_count
        if data < 1:
            raise exceptions.NotFound("Документ не найден")
        return Response({"count": str(data)})

    @action(detail=False, methods=['post'], url_path="many")
    def create_many(self, request, *args, **kwargs):
        created = []
        for user in request.data:
            for doc_type in request.data[user]:
                for doc in request.data[user][doc_type]:
                    if db_docs[doc_type].find_one({"num": doc["num"]}) is None:
                        data = db_docs[doc_type].insert_one(doc).inserted_id
                        created.append(str(data))
        return Response(created)