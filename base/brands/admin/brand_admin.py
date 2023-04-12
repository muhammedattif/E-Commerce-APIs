# Django Imports
from django.contrib import admin

# First Party Imports
from base.brands.models import Brand
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(Brand)
class BrandAdmin(AbstractModelAdmin):
    list_display = ["id", "seller", "name"]
    list_filter = ["seller__email", "name"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["seller"]
