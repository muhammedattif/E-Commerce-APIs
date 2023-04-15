# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.admin_forms import ModelFormWithApproval
from base.products.models import ModelApproval, ProductApproval
from base.utility.utility_admin import (
    AbstractModelAdmin,
    AbstractModelAdminWithApprovalInlineMixin,
    AbstractModelAdminWithApprovalMixin,
    AbstractStackedInline,
)


class ModelApprovalInline(AbstractModelAdminWithApprovalInlineMixin, AbstractStackedInline):
    model = ModelApproval
    form = ModelFormWithApproval
    extra = 0
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


@admin.register(ProductApproval)
class ProductApprovalAdmin(AbstractModelAdminWithApprovalMixin, AbstractModelAdmin):
    list_display = [
        "seller",
        "name",
        "category",
        "type",
        "is_sale",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "seller",
        "name",
        "category",
        "type",
        "created_at",
        "updated_at",
    ]
    fields = [
        "name",
        "description",
        "about",
        "category",
        "collection_name",
        "material",
        "type",
        "size_guide",
        "seller",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "seller",
        "created_at",
        "updated_at",
    ]
    autocomplete_fields = ["category"]
    search_fields = ["name", "description", "about"]
    ordering = ["-created_at"]
    list_select_related = ["seller", "category"]
    inlines = [ModelApprovalInline]
