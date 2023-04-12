# Django Imports
from django.contrib import admin

# First Party Imports
from base.users.models import SecretToken
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(SecretToken)
class SecretTokenAdmin(AbstractModelAdmin):
    list_display = ["id", "token_type", "lifetime", "expires_at", "key", "is_active", "created_at"]
    list_filter = ["created_at", "expires_at", "token_type"]
    readonly_fields = ["key", "created_at", "updated_at"]
    ordering = ["-id"]
    fields = [
        "token_type",
        "lifetime",
        "expires_at",
        "key",
        "is_active",
        "created_at",
        "updated_at",
    ]
