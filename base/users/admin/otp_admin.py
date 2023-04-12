# Django Imports
from django.contrib import admin

# First Party Imports
from base.users.models import OTP
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(OTP)
class OTPAdmin(AbstractModelAdmin):
    list_display = ("id", "user", "email", "expires_at", "otp_type", "pin", "is_active", "created_at")
    list_filter = (
        "created_at",
        "expires_at",
        "otp_type",
        "is_active",
    )
    fields = [
        "otp_type",
        "expires_at",
        "user",
        "email",
        "is_active",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ("created_at", "updated_at")
    search_fields = ["pin", "user__username"]
    list_select_related = ("user",)
