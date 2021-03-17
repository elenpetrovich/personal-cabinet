from rest_framework import serializers
from .models import DocumentFile


class DocumentFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = DocumentFile
        fields = (
            'id',
            'mongodb_id',
            'company',
            'saved',
            'file_path',
            'requested_date',
            'saved_file_date',
        )
        read_only_fields = (
            'id',
            'company',
            'saved',
        )


class FileUploadSerializers(serializers.Serializer):
    file_data = serializers.FileField()
    file_ref = serializers.SlugField()
    file_format = serializers.SlugField()
    file_rule = serializers.CharField()
    company = serializers.CharField()
