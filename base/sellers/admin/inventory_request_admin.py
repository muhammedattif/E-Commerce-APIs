# Django Imports
from django.contrib import admin, messages

# First Party Imports
from base.sellers.models import InventoryRequest
from base.sellers.utils.choices import InventoryRequestStatusChoices
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(InventoryRequest)
class InventoryRequestAdmin(AbstractModelAdmin):
    list_display = [
        "id",
        "type",
        "seller",
        "model",
        "quantity",
        "is_approved",
        "approved_by",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "type",
        "seller",
        "model",
        "quantity",
        "is_approved",
        "approved_by",
        "approved_at",
        "is_active",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["is_approved", "approved_at", "approved_by", "created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["seller", "model", "approved_by"]
    actions = ["approve"]

    def approve(self, request, queryset):
        for inventory_request in queryset:
            is_approved, status = inventory_request.approve(user=request.user)
            if is_approved:
                message = "Request: {0} {1}".format(
                    inventory_request.__str__(),
                    InventoryRequestStatusChoices(status).label,
                )
                self.message_user(request, message, level=messages.SUCCESS)
            else:
                message = "Request: {0} {1}".format(
                    inventory_request.__str__(),
                    InventoryRequestStatusChoices(status).label,
                )
                self.message_user(request, message, level=messages.ERROR)
        return
