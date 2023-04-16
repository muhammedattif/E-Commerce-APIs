# Django Imports
from django.contrib import admin

# First Party Imports
from base.brands.models import BrandTracker
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(BrandTracker)
class BrandTrackerAdmin(AbstractModelAdmin):
    list_display = ["id", "user", "brand"]
    list_filter = ["user", "brand"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["user", "brand"]
