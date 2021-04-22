from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action
from .models import Collection, Company, Role
from .serializers import CompanySerializer, CollectionSerializer, RoleSerializer


class CollectionViewSet(viewsets.GenericViewSet):
    queryset = Collection.objects
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoleViewSet(viewsets.GenericViewSet):
    queryset = Role.objects
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'


class CompanyViewSet(viewsets.GenericViewSet):
    queryset = Company.objects
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'system_name'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset.filter().all())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"company_list": serializer.data},
                        template_name="company_list.html")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        collection_queryset = Collection.objects.filter(company=instance).all()
        collection_serializer = CollectionSerializer(collection_queryset,
                                                     many=True)
        return Response(
            {
                "company": serializer.data,
                "collection_list": collection_serializer.data
            },
            template_name="collection_list.html",
        )
