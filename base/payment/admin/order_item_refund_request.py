# Django Imports
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.payment.models import OrderItemRefundRequest
from base.utility.choices import ApprovalActionChoices
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(OrderItemRefundRequest)
class OrderItemRefundRequestAdmin(AbstractModelAdmin):
    list_display = [
        "item",
        "status",
        "additional_info",
        "action_taken_by",
        "action_taken_at",
    ]
    list_filter = [
        "id",
        "item__order__user",
        "status",
        "action_taken_by",
        "action_taken_at",
    ]
    search_fields = [
        "item__product__name",
        "item__product__description",
    ]
    actions = ["approve", "decline"]

    fieldsets = (
        (
            _("Refund Request Information"),
            {
                "fields": (
                    "item",
                    "quantity",
                    "item_price",
                    "additional_info",
                    "status",
                    "action_taken_by",
                    "action_taken_at",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
        (
            _("Order Information"),
            {
                "fields": (
                    "order_reference",
                    "order_created_at",
                ),
            },
        ),
        (
            _("User Information"),
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                ),
            },
        ),
    )

    readonly_fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "status",
        "action_taken_by",
        "action_taken_at",
        "created_at",
        "updated_at",
        "order_created_at",
        "order_reference",
        "item_price",
    )

    @staticmethod
    def email(obj):
        return obj.item.order.email

    @staticmethod
    def first_name(obj):
        return obj.item.order.first_name

    @staticmethod
    def last_name(obj):
        return obj.item.order.last_name

    @staticmethod
    def phone_number(obj):
        return obj.item.order.phone_number

    @staticmethod
    def order_reference(obj):
        return obj.item.order.id

    @staticmethod
    def order_created_at(obj):
        return obj.item.order.created_at

    @staticmethod
    def item_price(obj):
        return obj.item.price * obj.quantity

    @admin.display(description=_("Approve"))
    def approve(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(
                request,
                _("You must select one Request at a time."),
                level=40,
            )
            return

        item_refund_request = queryset.first()
        if item_refund_request.status == ApprovalActionChoices.APPROVED:
            self.message_user(request, _("Request Already Approved."), level=messages.ERROR)
            return

        elif item_refund_request.status == ApprovalActionChoices.DECLINED:
            self.message_user(request, _("Request Already Declined."), level=messages.ERROR)
            return

        is_approved = item_refund_request.approve(action_user=request.user)
        if not is_approved:
            self.message_user(request, _("Cannot Approve Request."), level=messages.ERROR)
        else:
            self.message_user(request, _("Request Approved Successfully."), level=messages.SUCCESS)
        return

    @admin.display(description=_("Decline"))
    def decline(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(
                request,
                _("You must select one Request at a time."),
                level=40,
            )
            return

        item_refund_request = queryset.first()
        if item_refund_request.status == ApprovalActionChoices.APPROVED:
            self.message_user(request, _("Request Already Approved."), level=messages.ERROR)
            return

        elif item_refund_request.status == ApprovalActionChoices.DECLINED:
            self.message_user(request, _("Request Already Declined."), level=messages.ERROR)
            return

        is_declined = item_refund_request.decline(action_user=request.user)
        if not is_declined:
            self.message_user(request, _("Cannot Decline Request."), level=messages.ERROR)
        else:
            self.message_user(request, _("Request Declined Successfully."), level=messages.SUCCESS)
        return
