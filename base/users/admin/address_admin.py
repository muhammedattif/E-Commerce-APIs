# Django Imports
from django.contrib import admin

# First Party Imports
from base.users.models import Address
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(Address)
class AddressAdmin(AbstractModelAdmin):
    list_display = ["user", "first_name", "last_name", "email", "phone_number", "is_primary", "country"]
    list_filter = ["user", "first_name", "last_name", "email", "phone_number", "is_primary", "country"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
