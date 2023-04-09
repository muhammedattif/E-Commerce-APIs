# Django Imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# First Party Imports
from base.users.models import User
from base.utility.utility_admin import AdminListPerPageMixin


@admin.register(User)
class UserAdmin(AdminListPerPageMixin, UserAdmin):
    list_filter = [
        "email",
        "first_name",
        "last_name",
        "gender",
        "last_login",
        "last_logout",
        "last_action",
        "birth_date",
        "created_at",
        "updated_at",
        "is_staff",
        "is_guest",
        "is_seller",
        "is_buyer",
        "is_suspended",
        "is_email_verified",
        "is_online",
        "is_staff",
        "is_active",
    ]
    ordering = ["-created_at"]
    readonly_fields = [
        "last_login",
        "last_logout",
        "last_action",
        "created_at",
        "updated_at",
    ]
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_email_verified",
        "is_seller",
        "is_buyer",
        "is_online",
        "is_staff",
        "is_active",
        "created_at",
    )
    search_fields = (
        "email" "first_name",
        "last_name",
    )
    fieldsets = (
        (
            "User Information",
            {
                "fields": (
                    "email",
                    "is_email_verified",
                    "first_name",
                    "last_name",
                    "gender",
                    "referral_code",
                    "last_login",
                    "last_logout",
                    "last_action",
                    "birth_date",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_guest",
                    "is_seller",
                    "is_buyer",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Password", {"fields": ("password",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
