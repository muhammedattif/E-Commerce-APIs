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
        "status",
        "action_taken_at",
        "action_taken_by",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "type",
        "seller",
        "model",
        "quantity",
        "status",
        "action_taken_at",
        "action_taken_by",
        "is_active",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "status",
        "action_taken_at",
        "action_taken_by",
        "created_at",
        "updated_at",
    ]
    ordering = ["-created_at"]
    list_select_related = ["seller", "model", "action_taken_by"]
    actions = ["approve", "decline"]

    def approve(self, request, queryset):
        for inventory_request in queryset:
            is_approved, status = inventory_request.approve(action_user=request.user)
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

    def decline(self, request, queryset):
        for inventory_request in queryset:
            is_declined, status = inventory_request.decline(action_user=request.user)
            if is_declined:
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
