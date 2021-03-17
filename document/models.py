from django.http import request
from pymongo import MongoClient
from mysite.settings import MONGODB
from django.db import models

client = MongoClient(MONGODB)
db_docs = client['documents']


class DocumentFile(models.Model):
    mongodb_id = models.CharField("ObjectID", max_length=25)
    documet_ref = models.CharField("Ref", max_length=25)
    company = models.ForeignKey("cabinet.Company", on_delete=models.CASCADE)
    saved = models.BooleanField("Сохранен", default=False)
    file_path = models.FileField("Название",
                                 max_length=254,
                                 null=True,
                                 default=None)
    requested_date = models.DateTimeField("Заявка создана", auto_now_add=True)
    saved_file_date = models.DateTimeField("Файл сохранен")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'documet_ref'],
                                    name='unique_company_document'),
        ]

    def __str__(self) -> str:
        return f"{self.mongodb_id} {self.company} статус: {self.saved}"