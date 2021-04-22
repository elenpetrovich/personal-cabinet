from rest_framework import serializers
from .models import Company, Role, Collection


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            "system_name",
            "short_name",
            "full_name",
            "city",
            "address",
            "email",
            "public",
        )
        read_only_fields = ('id', )


class CompanyShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            "system_name",
            "short_name",
            "full_name",
            "public",
        )
        read_only_fields = ('id', )


class CollectionSerializer(serializers.ModelSerializer):
    company = CompanyShortSerializer()

    class Meta:
        model = Collection
        fields = ('id', 'company', 'name')


class RoleSerializer(serializers.ModelSerializer):
    company = CompanyShortSerializer()

    class Meta:
        model = Role
        fields = ('id', 'company', 'name')
        depth = 1
