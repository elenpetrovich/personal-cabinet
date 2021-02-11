from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = (
            'id',
            'last_login',
            'is_superuser',
            'is_staff',
            'is_active',
            'date_joined',
            'groups',
            'user_permissions',
            'password',
            'first_name',
            'last_name',
            'email',
        )

    def create(self, validated_data):
        return Account.objects.create(password=Account.random_password(),
                                      **validated_data)
