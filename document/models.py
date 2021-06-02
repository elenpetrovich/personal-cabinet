from os import path
from django.contrib.auth.models import User
from django.http import request
from pymongo import MongoClient
from django.db import models
import uuid

from pathlib import Path
import posixpath
from django.utils._os import safe_join
from django.conf import settings

from mysite.settings import MONGODB

client = MongoClient(MONGODB)


class Document(models.Model):
    id = models.SlugField("ObjectID", max_length=24, primary_key=True)
    ref = models.SlugField("Ref", max_length=36)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Изменен", auto_now=True)
    collection = models.ForeignKey("company.Collection",
                                   on_delete=models.CASCADE,
                                   related_name="docs")
    is_public = models.BooleanField("Публичность", default=False)

    file_folder = models.CharField("Путь до папки с файлами",
                                   max_length=1023,
                                   null=True,
                                   blank=True,
                                   default="")

    roles = models.ManyToManyField("company.Role", related_name="docs")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ref', 'collection'],
                                    name='unique_ref_collection'),
        ]

    def __str__(self) -> str:
        return f"{self.id} {self.collection}"

    def default_folder_name(
        self,
        company_name=None,
        collection_name=None,
        folder_name=None,
    ):
        if not folder_name:
            folder_name = self.id
        if company_name and collection_name:
            return f"{company_name}/{collection_name}/{folder_name}"
        return f"docs/{folder_name}"

    @property
    def folder(self) -> Path:
        return Path(
            safe_join(
                settings.MEDIA_ROOT,
                posixpath.normpath(f"{self.file_folder}/").lstrip('/'),
            ))

    @folder.setter
    def folder(self, name: str):
        self.file_folder = self.default_folder_name(folder_name=name)


class RequestDoc(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document,
                                 on_delete=models.CASCADE,
                                 related_name="request_list")
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="request_list")
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)
    text = models.TextField("Сообщение", null=True)
    kind = models.IntegerField(
        "Тип запроса")  # 0 - неопределенно, 1 - файл, 2 - редактирование
    is_solved = models.BooleanField("Исполнено", default=False)
    solved_at = models.DateTimeField("Дата исполнения", null=True, blank=True)