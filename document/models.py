from django.contrib.auth.models import Group
from django.http import request
from pymongo import MongoClient
from django.db import models
import uuid

from mysite.settings import MONGODB

client = MongoClient(MONGODB)


class Document(models.Model):
    id = models.SlugField("ObjectID", max_length=24, primary_key=True)
    ref = models.SlugField("Ref", max_length=34)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Изменен", auto_now=True)
    collection = models.ForeignKey("company.Collection",
                                   on_delete=models.CASCADE,
                                   related_name="docs")
    is_public = models.BooleanField("Публичность", default=False)

    file_folder = models.FileField("Путь до папки с файлами",
                                   max_length=254,
                                   null=True,
                                   default=None)

    roles = models.ManyToManyField("company.Role", related_name="docs")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ref', 'collection'],
                                    name='unique_ref_collection'),
        ]

    def __str__(self) -> str:
        return f"{self.id} {self.collection}"


class RequestDoc(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document,
                                 on_delete=models.CASCADE,
                                 related_name="request_files")
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)
    text = models.TextField("Сообщение", null=True)
    kind = models.IntegerField(
        "Тип запроса")  # 0 - неопределенно, 1 - файл, 2 - редактирование
    is_solved = models.BooleanField("Исполнено", default=False)
    solved_at = models.DateTimeField("Дата исполнения")