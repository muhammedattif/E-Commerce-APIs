# Django Imports
from django.contrib import admin

# First Party Imports
from base.utility.models import Governorate
from base.utility.utility_admin import AdminListPerPageMixin


@admin.register(Governorate)
class GovernorateAdmin(AdminListPerPageMixin, admin.ModelAdmin):
    list_display = ["id", "en_name", "ar_name", "created_at", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["id", "en_name", "ar_name"]
    readonly_fields = ["created_at"]
    ordering = ["en_name"]
