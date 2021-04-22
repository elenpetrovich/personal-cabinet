from rest_framework import serializers
from company.models import Company


class DynamicFieldsSerializer():
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CompanyUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'system_name',
            'short_name',
            'full_name',
            'city',
            'address',
            'email',
            'public',
            'secret_key',
        )
        read_only_fields = ('id', 'system_name')


class UserUploadSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(allow_blank=True, required=False)
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    email = serializers.CharField(allow_blank=True, required=False)


class CollectionUploadSerializer(serializers.Serializer):
    name = serializers.CharField()
    mongo_collection = serializers.CharField()


# class DocUploadSerializer(serializers.Serializer):
#     ref = serializers.SlugField()


class DocListUploadSerializer(serializers.Serializer):
    name = serializers.CharField()
    link_name = serializers.CharField()
    docs = serializers.ListField(child=serializers.DictField(),
                                 allow_empty=True)
    prune_old = serializers.BooleanField(required=False, default=False)


class RoleUploadSerializer(serializers.Serializer):
    name = serializers.CharField()
    collections_list = serializers.ListField(child=serializers.CharField(),
                                             allow_empty=True)
    username_list = serializers.ListField(child=serializers.CharField(),
                                          allow_empty=True)
    prune_old_users = serializers.BooleanField(required=False, default=False)
    prune_old_collections = serializers.BooleanField(required=False,
                                                     default=False)


class FileUploadSerializers(serializers.Serializer):
    file_data = serializers.FileField()
    file_ref = serializers.CharField()
    collection = serializers.CharField()


class FileRequestSerializers(serializers.ModelSerializer):
    pass


#     class Meta:
#         model = DocumentFile
#         fields = (
#             'id',
#             'saved',
#             'ref',
#             'collection',
#             'requested_date',
#         )
#         read_only_fields = ('id')