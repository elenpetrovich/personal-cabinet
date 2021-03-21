from django.contrib import admin
from .models import DocumentFile, DocumentPermissions


@admin.register(DocumentFile, DocumentPermissions)
class DocumentAdmin(admin.ModelAdmin):
    pass
