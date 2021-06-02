from rest_framework import serializers
from company.models import Company, Collection
from document.models import RequestDoc


class CompanyUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'system_name',
            'url_name',
            'short_name',
            'full_name',
            'city',
            'address',
            'email',
            'is_public',
            'inn',
            'kpp',
            'ogrp',
            'okpo',
        )
        read_only_fields = ('id', 'system_name', 'url_name')


class UserUploadSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(allow_blank=True, required=False)
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    email = serializers.CharField(allow_blank=True, required=False)


class CollectionUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'id',
            'url_name',
            'public_name',
            'link_name',
            'schema',
        )
        read_only_fields = ('id', )


class RoleUploadSerializer(serializers.Serializer):
    name = serializers.CharField()
    collections_list = serializers.ListField(child=serializers.CharField(),
                                             allow_empty=True)
    username_list = serializers.ListField(child=serializers.CharField(),
                                          allow_empty=True)
    delete_old_users = serializers.BooleanField(required=False, default=False)
    delete_old_collections = serializers.BooleanField(required=False,
                                                      default=False)


class DocListUploadSerializer(serializers.Serializer):
    url_name = serializers.CharField()
    docs = serializers.ListField(child=serializers.DictField(),
                                 allow_empty=True)
    role_list = serializers.ListField(child=serializers.CharField(),
                                      allow_empty=True)
    delete_old = serializers.BooleanField(required=False, default=False)


class FileUploadSerializers(serializers.Serializer):
    file_data = serializers.FileField()
    file_name = serializers.CharField(required=False, default="")
    ref = serializers.CharField()
    collection = serializers.CharField()


class RequestDocUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestDoc
        fields = '__all__'
        read_only_fields = (
            'created_at',
            'document',
            'user',
            'id',
            'text',
            'kind',
        )