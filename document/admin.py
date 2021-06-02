from django.contrib import admin
from .models import Document, RequestDoc


@admin.register(Document, RequestDoc)
class DocumentAdmin(admin.ModelAdmin):
    pass
