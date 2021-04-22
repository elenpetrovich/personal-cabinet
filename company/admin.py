from django.contrib import admin

from .models import Company, Role, Collection


@admin.register(Company, Collection, Role)
class CompanyAdmin(admin.ModelAdmin):
    pass
