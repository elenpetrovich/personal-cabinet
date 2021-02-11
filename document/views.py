from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, mixins, views, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import db_docs


class DocumentViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path="search")
    def search(self, request, *args, **kwargs):
        title = request.query_params.get('title')
        data = db_docs["test-1c"].find({"Заголовок": title})
        return Response(list(data))

    def list(self, request, pk=None):
        data = db_docs["test-1c"].find()
        print(data)
        print(list(data))
        return Response(list(data))