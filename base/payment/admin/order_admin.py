# Django Imports
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.payment.models import Order, OrderItem, OrderTracker
from base.payment.utils.choices import OrderStatusChoices, PaymentTypesChoices
from base.utility.utility_admin import AbstractModelAdmin, AbstractStackedInline


class OrderItemInline(AbstractStackedInline):
    model = OrderItem
    can_delete = False
    verbose_name_plural = "Items"

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class OrderTrackerInline(AbstractStackedInline):
    model = OrderTracker
    verbose_name_plural = "Tracking"
    extra = 0
    fields = ("status", "estimated_date", "additional_info", "created_at")
    readonly_fields = ("created_at",)

    def has_add_permission(self, request, obj=None):
        return super(OrderTrackerInline, self).has_add_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return super(OrderTrackerInline, self).has_change_permission(request, obj)


@admin.register(Order)
class OrderAdmin(AbstractModelAdmin):
    list_filter = (
        "status",
        "user",
        "sub_total",
        "total",
        "discount",
        "taxes",
        "payment_type",
        "provider",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "user",
        "status",
        "payment_type",
        "provider",
        "address",
        "sub_total",
        "total",
        "discount",
        "taxes",
        "created_at",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "status",
                    "sub_total",
                    "total",
                    "discount",
                    "taxes",
                    "payment_type",
                    "provider",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
        (
            _("Shipping Address"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "street_1",
                    "street_2",
                    "landmark",
                    "country",
                    "governorate",
                    "city",
                    "additional_info",
                ),
            },
        ),
    )

    search_fields = ("items__product__name", "items__product__description")
    readonly_fields = (
        "user",
        "sub_total",
        "total",
        "discount",
        "taxes",
        "payment_type",
        "provider",
        "created_at",
        "updated_at",
    )
    list_select_related = ("user", "address")
    ordering = ["-created_at"]
    inlines = [OrderItemInline]
    actions = ["cancel", "confirm"]

    def get_inlines(self, request, obj):
        inlines = []
        if not obj:
            return []
        elif obj.status in OrderStatusChoices.fail_status_set() or obj.payment_type == PaymentTypesChoices.COD:
            inlines += [OrderTrackerInline]
        else:
            messages.warning(
                request,
                _(
                    """
                    This order has no transaction yet. 
                    Once transaction is added you will be able to add tracking info to this order.
                    """,
                ),
            )
        return super().get_inlines(request, obj) + inlines

    def get_readonly_fields(self, request, obj=None):
        add_read_only = ()
        if obj and obj.status != OrderStatusChoices.INITIATED:
            add_read_only += ("status",)
        return self.readonly_fields + add_read_only

    @admin.display(description=_("Cancel"))
    def cancel(self, request, queryset):
        for order in queryset:
            is_cancelled = order.cancel()
            if is_cancelled:
                self.message_user(
                    request,
                    _("Order: #{0} Cancelled Successfully.").format(order.id),
                    level=messages.SUCCESS,
                )
            else:
                self.message_user(
                    request,
                    _("Cannot Cancel Order: #{0}.").format(order.id),
                    level=messages.ERROR,
                )

            return

    @admin.display(description=_("Confirm"))
    def confirm(self, request, queryset):
        for order in queryset:
            is_confirmed = order.confirm()
            if is_confirmed:
                self.message_user(
                    request,
                    _("Order: #{0} Confirmed Successfully").format(order.id),
                    level=messages.SUCCESS,
                )
            else:
                self.message_user(
                    request,
                    _("Order: #{0} Cannot be Confirmed.").format(order.id),
                    level=messages.ERROR,
                )
            return
