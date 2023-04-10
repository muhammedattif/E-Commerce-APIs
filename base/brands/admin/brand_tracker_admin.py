# Django Imports
from django.contrib import admin

# First Party Imports
from base.brands.models import BrandTracker
from base.utility.utility_admin import AdminListPerPageMixin


@admin.register(BrandTracker)
class BrandTrackerAdmin(AdminListPerPageMixin, admin.ModelAdmin):
    list_display = ["id", "user", "brand", "clicks"]
    list_filter = ["user", "brand"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
