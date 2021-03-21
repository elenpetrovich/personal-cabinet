from django.db import models
from django.contrib.auth.models import User, Group
import string
import random
from django.db.models import Count
from django.contrib.auth.backends import ModelBackend


class Company(models.Model):
    name = models.CharField("Название", max_length=254)
    city = models.CharField("Город", max_length=254)
    address = models.CharField("Адрес", max_length=254)
    email = models.EmailField("Электронная почта")
    mongodb_collection = models.CharField("collection", max_length=254)
    public = models.BooleanField("Публичность", default=False)
    secret_key = models.CharField("Ключ доступа", max_length=254)
    password = models.CharField("Пароль", max_length=254)

    def __str__(self) -> str:
        return f"{self.name} г. {self.city}"


class Role(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    company = models.ForeignKey("cabinet.Company",
                                on_delete=models.CASCADE,
                                null=True,
                                related_name="roles")

    def __str__(self) -> str:
        return f"{self.group} ({self.company})"


class Account(User):
    class Meta:
        proxy = True

    def get_roles(self, company: str = None, group: str = None):
        if company is None:
            return Role.objects.filter(group__user=self).all()
        elif group is None:
            return Role.objects.filter(group__user=self,
                                       company__name=company).all()
        else:
            return Role.objects.filter(group__user=self,
                                       company__name=company,
                                       group__name=group).all()

    def get_companies(self, company: str = None, group: str = None):
        if company is None:
            return Company.objects.filter(
                roles__group__user=self).distinct().all()
        elif group is None:
            return Company.objects.filter(
                name=company, roles__group__user=self).distinct().all()
        else:
            return Company.objects.filter(
                name=company,
                roles__group__user=self,
                roles__group__name=group).distinct().all()


class AccountModelBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
