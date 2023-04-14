# Django Imports
from django.contrib import admin, messages

# First Party Imports
from base.sellers.models import InventoryRequest
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(InventoryRequest)
class InventoryRequestAdmin(AbstractModelAdmin):
    list_display = [
        "id",
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
            is_approved = inventory_request.approve(user=request.user)
            if is_approved:
                message = "Request: {0} Approved Successfully".format(inventory_request.__str__())
                self.message_user(request, message, level=messages.SUCCESS)
            else:
                message = "Request: {0} is Already Approved".format(inventory_request.__str__())
                self.message_user(request, message, level=messages.ERROR)
        return
