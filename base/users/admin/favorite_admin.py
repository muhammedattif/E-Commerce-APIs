# Django Imports
from django.contrib import admin

# First Party Imports
from base.users.models import Favorite
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(Favorite)
class FavoriteAdmin(AbstractModelAdmin):
    list_display = ["user", "created_at", "updated_at", "is_active"]
    list_filter = ["user", "created_at", "updated_at", "is_active"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
