from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.backends import ModelBackend

from company.models import Collection, Role, Company


class Account(User):
    class Meta:
        proxy = True

    def get_roles(self, company: str = None, role: str = None):
        if company is None:
            return Role.objects.filter(users=self).all()
        elif role is None:
            return Role.objects.filter(users=self, system_name=company).all()
        else:
            return Role.objects.filter(users=self,
                                       system_name=company,
                                       name=role).all()

    def get_companies(self, company: str = None, role: str = None):
        if company is None:
            return Company.objects.filter(roles__users=self).distinct().all()
        elif role is None:
            return Company.objects.filter(system_name=company,
                                          roles__users=self).distinct().all()
        else:
            return Company.objects.filter(system_name=company,
                                          roles__users=self,
                                          roles__name=role).distinct().all()

    def get_collection(self, company: str = None, collection: str = None):
        return Company.objects.filter(system_name=company,
                                      roles__users=self).distinct().all()


class AccountModelBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None


class RegistrationRequest(models.Model):
    fio = models.CharField("ФИО", max_length=511)
    email = models.EmailField("Электронная почта")
    phone = models.CharField("Номер телефона", max_length=12)
    date = models.DateTimeField("Дата", auto_now_add=True)
    ip = models.GenericIPAddressField("IP")