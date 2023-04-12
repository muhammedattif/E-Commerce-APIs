# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.models import ModelOption
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(ModelOption)
class ModelOptionAdmin(AbstractModelAdmin):
    list_display = ["id", "name", "model_feature"]
    list_filter = ["name", "model_feature"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["model_feature"]
