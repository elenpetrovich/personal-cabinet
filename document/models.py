from django.contrib.auth.models import Group
from django.http import request
from pymongo import MongoClient
from mysite.settings import MONGODB
from django.db import models

client = MongoClient(MONGODB)
db_docs = client['documents']


class DocumentFile(models.Model):
    saved = models.BooleanField("Сохранен", default=False)
    file_path = models.FileField("Название",
                                 max_length=254,
                                 null=True,
                                 default=None)
    requested_date = models.DateTimeField("Заявка создана", auto_now_add=True)
    saved_file_date = models.DateTimeField("Файл сохранен")

    def __str__(self) -> str:
        return f"{self.file_path}"


class DocumentPermissions(models.Model):
    mongodb_id = models.SlugField("ObjectID", max_length=25)
    documet_ref = models.SlugField("Ref", max_length=37)
    company = models.ForeignKey("cabinet.Company", on_delete=models.CASCADE)
    created = models.DateTimeField("Создан", auto_now_add=True)
    updated = models.DateTimeField("Изменен", auto_now=True)
    file = models.OneToOneField("DocumentFile",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    groups = models.ManyToManyField(Group)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'documet_ref'],
                                    name='unique_company_document'),
        ]

    def __str__(self) -> str:
        return f"{self.mongodb_id} {self.documet_ref} {self.company}"