from django.contrib import admin
from .models import AccountController, RegistrationRequest


@admin.register(AccountController, RegistrationRequest)
class CabinetAdmin(admin.ModelAdmin):
    pass
