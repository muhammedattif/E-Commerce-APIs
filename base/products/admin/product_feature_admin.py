# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.models import ProductFeature, ProductOption
from base.utility.utility_admin import AbstractModelAdmin


class ProductOptionInline(admin.StackedInline):
    model = ProductOption
    extra = 0


@admin.register(ProductFeature)
class ProductFeatureAdmin(AbstractModelAdmin):
    list_display = ["id", "name", "product"]
    list_filter = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["product"]
    inlines = [ProductOptionInline]
