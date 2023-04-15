# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.admin_forms import ModelFormWithApproval
from base.products.models import ModelApproval
from base.utility.utility_admin import AbstractModelAdmin, AbstractModelAdminWithApprovalMixin


@admin.register(ModelApproval)
class ModelApprovalAdmin(AbstractModelAdminWithApprovalMixin, AbstractModelAdmin):
    form = ModelFormWithApproval
    list_display = [
        "product",
        "inventory_quantity",
        "price",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "product",
        "inventory_quantity",
        "price",
        "is_active",
        "created_at",
        "updated_at",
    ]
    fields = [
        "product",
        "product_options",
        "inventory_quantity",
        "price",
        "is_active",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["product"]
