# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.models import ModelTracker
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(ModelTracker)
class ModelTrackerAdmin(AbstractModelAdmin):
    list_display = ["id", "user", "model", "clicks"]
    list_filter = ["user", "model"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["user", "model"]
