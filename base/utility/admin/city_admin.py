# Django Imports
from django.contrib import admin

# First Party Imports
from base.utility.models import City
from base.utility.utility_admin import AdminListPerPageMixin


@admin.register(City)
class CityAdmin(AdminListPerPageMixin, admin.ModelAdmin):
    list_display = ["id", "en_name", "ar_name", "governorate", "created_at", "is_active"]
    list_filter = ["governorate", "is_active"]
    search_fields = ["id", "en_name", "ar_name", "governorate__en_name", "governorate__ar_name"]
    readonly_fields = ["created_at"]
    ordering = ["en_name"]
    list_select_related = ["governorate"]
