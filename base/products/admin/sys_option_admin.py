# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.models import SysOption
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(SysOption)
class SysOptionAdmin(AbstractModelAdmin):
    list_display = ["id", "name", "sys_feature"]
    list_filter = ["name", "sys_feature"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["sys_feature"]
