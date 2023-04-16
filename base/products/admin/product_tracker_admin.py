# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.models import ProductTracker
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(ProductTracker)
class ProductTrackerAdmin(AbstractModelAdmin):
    list_display = ["id", "user", "product"]
    list_filter = ["user", "product"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["user", "product"]
