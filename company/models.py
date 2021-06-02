from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from pymongo import collection


class Company(models.Model):
    system_name = models.SlugField(
        "Уникальное название",
        max_length=254,
        unique=True,
    )
    url_name = models.CharField(
        "URL название",
        max_length=254,
        validators=[RegexValidator(r"^[a-zA-Z0-9а-яА-Я_-]+\Z")])
    email = models.EmailField("Электронная почта")
    mongo_db = models.CharField("MongoDB", max_length=254)
    is_public = models.BooleanField("Публичность", default=False)
    secret_key = models.SlugField("Ключ доступа", max_length=254)

    short_name = models.CharField("Короткое название", max_length=254)
    full_name = models.CharField("Полное название", max_length=510)
    city = models.CharField("Город", max_length=254)
    address = models.CharField("Адрес", max_length=254)
    inn = models.CharField("ИНН", max_length=12, null=True, blank=True)
    kpp = models.CharField("КПП", max_length=12, null=True, blank=True)
    ogrp = models.CharField("ОГРН", max_length=15, null=True, blank=True)
    okpo = models.CharField("ОКПО", max_length=12, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.short_name} г. {self.city}"


class Collection(models.Model):
    url_name = models.CharField(
        "URL название",
        max_length=254,
        validators=[RegexValidator(r"^[a-zA-Z0-9а-яА-Я_-]+\Z")])
    public_name = models.CharField("Название", max_length=254)
    link_name = models.CharField("Ссылка", max_length=254)
    schema = models.JSONField("Схема", default=dict)
    # schema example: {"Название": {"position": 0, "template": "<div class="border">{name}</div>: <div class="mx-3">{value}</div>"}}
    mongo_collection = models.CharField("MongoDB", max_length=254)
    company = models.ForeignKey("company.Company",
                                on_delete=models.CASCADE,
                                related_name="collections")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['url_name', 'company'],
                                    name='unique_url_name_company'),
        ]

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'company'],
                                    name='unique_name_company'),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.company})"
