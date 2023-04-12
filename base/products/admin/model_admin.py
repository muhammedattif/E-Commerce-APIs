# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.models import Model
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(Model)
class ModelAdmin(AbstractModelAdmin):
    list_display = ["id", "seller", "name", "category", "type", "is_active", "created_at", "updated_at"]
    list_filter = [
        "seller",
        "name",
        "category",
        "type",
        "is_active",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["seller", "category"]
