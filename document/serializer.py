from rest_framework import serializers
from .models import RequestDoc


class RequestDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestDoc
        fields = '__all__'
        read_only_fields = (
            'created_at',
            'solved_at',
            'is_solved',
            'document',
            'user',
            'id',
        )