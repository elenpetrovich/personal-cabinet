from rest_framework import serializers
from .models import Account, RegistrationRequest


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


class RegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationRequest
        fields = '__all__'
        read_only_fields = (
            'id',
            'date',
            'ip',
        )