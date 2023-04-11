# Django Imports
from django.contrib import admin

# First Party Imports
from base.categories.models import Category
from base.utility.utility_admin import AdminListPerPageMixin


@admin.register(Category)
class CategoryAdmin(AdminListPerPageMixin, admin.ModelAdmin):
    list_display = ["id", "name", "parent"]
    list_filter = ["parent__name", "name"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
