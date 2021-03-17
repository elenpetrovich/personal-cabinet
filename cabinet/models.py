from django.db import models
from django.contrib.auth.models import User
import string
import random


class Account(User):
    class Meta:
        # app_label = 'account'
        proxy = True

    @classmethod
    def random_password(cls, size: int = 10):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for x in range(size))

    def set_random_password(self, size: int = 10):
        self.password = self.random_password(size=size)
        return self.password


class Company(models.Model):
    name = models.CharField("Название", max_length=254)
    city = models.CharField("Город", max_length=254)
    address = models.CharField("Адрес", max_length=254)
    email = models.EmailField("Электронная почта")
    users = models.ManyToManyField("cabinet.Account")
    mongodb_collection = models.CharField("collection", max_length=254)
    public = models.BooleanField("Публичность", default=False)
    secret_key = models.CharField("Ключ доступа", max_length=254)
    password = models.CharField("Пароль", max_length=254)

    def __str__(self) -> str:
        return self.name + " г. " + self.city
