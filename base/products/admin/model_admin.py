# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.admin_forms import ModelForm
from base.products.models import Model, ModelImage
from base.utility.utility_admin import AbstractModelAdmin, AbstractStackedInline


class ModelImageInline(AbstractStackedInline):
    model = ModelImage
    extra = 0


@admin.register(Model)
class ModelAdmin(AbstractModelAdmin):
    form = ModelForm
    list_display = [
        "id",
        "product",
        "inventory_quantity",
        "price",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "product",
        "inventory_quantity",
        "price",
        "is_active",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["product"]
    inlines = [ModelImageInline]
