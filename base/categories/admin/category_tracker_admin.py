# Django Imports
from django.contrib import admin

# First Party Imports
from base.categories.models import CategoryTracker
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(CategoryTracker)
class CategoryTrackerAdmin(AbstractModelAdmin):
    list_display = ["id", "user", "category"]
    list_filter = ["user", "category"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["user", "category"]
