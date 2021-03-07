from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, mixins, views, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import permissions

from .models import Account, Company
from .serializers import AccountSerializer, CompanySerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = Account.objects
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.get(id=request.user.id)
        serializer = self.get_serializer(queryset)
        return Response({"data": serializer.data}, template_name="user.html")


class CompanyViewSet(viewsets.GenericViewSet):
    queryset = Company.objects
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.queryset.filter(users=request.user).all())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data},
                        template_name="company_list.html")


@api_view(['GET', 'POST'])
def postData(request):
    print(request.data)
    data = request.data
    return Response(data=data)
