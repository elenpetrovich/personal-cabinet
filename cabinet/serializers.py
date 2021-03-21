from rest_framework import serializers
from .models import Account, Company, Role
from django.contrib.auth.models import Group

# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = (
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'email',
#             'is_active',
#             'groups',
#         )
#         read_only_fields = (
#             'id',
#             'is_active',
#             'groups',
#         )
#         depth = 3


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


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    group = GroupSerializer()

    class Meta:
        model = Role
        fields = ('id', 'company', 'group')
        depth = 1


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
