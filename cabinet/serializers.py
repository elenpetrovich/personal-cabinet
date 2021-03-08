from rest_framework import serializers
from .models import Account, Company


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'groups',
        )
        read_only_fields = (
            'id',
            'is_active',
            'groups',
        )


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            "name",
            "city",
            "address",
            "email",
            "public",
        )
        read_only_fields = ('id', )
