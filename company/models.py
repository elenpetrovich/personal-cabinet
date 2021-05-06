from django.db import models
from django.contrib.auth.models import User
from pymongo import collection


class Company(models.Model):
    system_name = models.SlugField(
        "Уникальное название",
        max_length=254,
        unique=True,
    )
    short_name = models.CharField("Короткое название", max_length=254)
    full_name = models.CharField("Полное название", max_length=510)
    city = models.CharField("Город", max_length=254)
    address = models.CharField("Адрес", max_length=254)
    email = models.EmailField("Электронная почта")
    mongo_db = models.CharField("MongoDB", max_length=254)
    is_public = models.BooleanField("Публичность", default=False)
    # TODO: ИНН КПП ?
    secret_key = models.SlugField("Ключ доступа", max_length=254)

    def __str__(self) -> str:
        return f"{self.system_name} {self.short_name} г. {self.city}"


class Collection(models.Model):
    public_name = models.CharField("Название", max_length=254)
    link_name = models.CharField("Ссылка", max_length=254)
    schema = models.JSONField("Схема", default=dict)
    mongo_collection = models.CharField("MongoDB", max_length=254)
    company = models.ForeignKey("company.Company",
                                on_delete=models.CASCADE,
                                related_name="collections")

    def __str__(self) -> str:
        return f"{self.public_name} ({self.company})"


class Role(models.Model):
    name = models.CharField("Название", max_length=254)
    company = models.ForeignKey("company.Company",
                                on_delete=models.CASCADE,
                                related_name="roles")
    users = models.ManyToManyField(User, related_name="roles")
    collections = models.ManyToManyField("company.Collection",
                                         related_name="roles")

    def __str__(self) -> str:
        return f"{self.name} ({self.company})"
