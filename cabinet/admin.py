from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

from .models import Company, Role


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group


class GroupInline(admin.StackedInline):
    model = Role
    can_delete = False
    verbose_name_plural = 'Company'


class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupInline, )


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
