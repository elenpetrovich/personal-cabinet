from rest_framework import serializers
from .models import Company, Role, Collection


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'url_name',
            "city",
            "address",
            "email",
            "address",
            "inn",
            "kpp",
            "ogrp",
            "okpo",
            "short_name",
            "full_name",
            "is_public",
        )
        read_only_fields = ('id', )


class CompanyShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            "short_name",
            "full_name",
            "is_public",
            'url_name',
        )
        read_only_fields = ('id', )


class CollectionSerializer(serializers.ModelSerializer):
    company = CompanyShortSerializer()

    class Meta:
        model = Collection
        fields = ('id', 'company', 'public_name', 'link_name', 'schema',
                  'url_name')
        read_only_fields = ('id', )


class RoleSerializer(serializers.ModelSerializer):
    company = CompanyShortSerializer()

    class Meta:
        model = Role
        fields = ('id', 'company', 'name')
        depth = 1
