# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.models import ProductOption
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(ProductOption)
class ProductOptionAdmin(AbstractModelAdmin):
    list_display = ["id", "name", "product_feature"]
    list_filter = ["name", "product_feature"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["product_feature"]
