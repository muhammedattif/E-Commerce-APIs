# Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# Other Third Party Imports
from django_countries.fields import CountryField

# First Party Imports
from base.payment.emails import OrderReciptEmail
from base.payment.utils.choices import (
    OrderItemStatusChoices,
    OrderStatusChoices,
    OrderTrackingStatusChoices,
    PaymentProvidersChoices,
    PaymentTypesChoices,
)
from base.utility.utility_models import AbstractModelWithHistory

from .order_tracker import OrderTracker


class Order(AbstractModelWithHistory):
    user = models.ForeignKey(
        "base.User",
        verbose_name=_("User"),
        on_delete=models.RESTRICT,
        related_name="orders",
    )
    total = models.FloatField(
        verbose_name=_("Total"),
    )
    sub_total = models.FloatField(
        verbose_name=_("Sub Total"),
    )
    discount = models.FloatField(
        default=0,
        verbose_name=_("Discount"),
    )
    taxes = models.FloatField(
        default=0,
        verbose_name=_("Taxes"),
    )
    status = models.IntegerField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.INITIATED,
    )
    payment_type = models.IntegerField(
        null=True,
        blank=True,
        choices=PaymentTypesChoices.choices,
        verbose_name=_("Payment Type"),
    )
    provider = models.IntegerField(
        choices=PaymentProvidersChoices.choices,
        null=True,
        blank=True,
        verbose_name=_("Provider"),
    )
    address = models.ForeignKey(
        "base.Address",
        null=True,
        blank=True,
        verbose_name=_("Address"),
        on_delete=models.SET_NULL,
    )
    # A copy of address data
    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        verbose_name=_("First name"),
    )
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        verbose_name=_("Last Name"),
    )
    email = models.EmailField(
        blank=True,
        null=True,
        max_length=60,
        verbose_name=_("Email"),
    )
    governorate = models.ForeignKey(
        "base.Governorate",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        max_length=30,
        verbose_name=_("Governorate"),
    )
    city = models.ForeignKey(
        "base.City",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        max_length=30,
        verbose_name=_("City"),
    )
    street_1 = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        verbose_name=_("Streat 1"),
    )
    street_2 = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        verbose_name=_("Streat 2"),
    )
    landmark = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        verbose_name=_("Landmark"),
    )
    phone_number = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        verbose_name=_("Phone Number"),
    )
    country = CountryField(
        blank=True,
        null=True,
        verbose_name=_("Country"),
    )
    additional_info = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Additional Info"),
    )

    class Meta:
        db_table = "payment_orders"
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return "Order Reference: #{0}".format(self.id)

    def clean_fields(self, **kwargs):

        old_order = self.__class__.objects.filter(id=self.id).last()
        if (
            old_order
            and old_order.status in OrderStatusChoices.fail_status_set()
            and self.status in OrderStatusChoices.success_status_set()
        ):
            raise ValidationError(
                {
                    "status": _("Order reached its final status."),
                },
            )
        super(Order, self).clean_fields(**kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Order, self).save(*args, **kwargs)

    @property
    def discount_percentage(self):
        return int((self.discount / self.sub_total) * 100)

    def cancel(self, is_failed=False):
        """Cancel order"""
        if self.status in OrderStatusChoices.fail_status_set():
            return False

        if is_failed:
            self.status = OrderStatusChoices.FAILED
        else:
            self.status = OrderStatusChoices.CANCELLED

        self.save()

        return True

    def confirm(self, is_failed=False):
        """Confirm order"""
        if self.status != OrderStatusChoices.INITIATED:
            return False

        self.status = OrderStatusChoices.CONFIRMED
        self.save()

        return True

    def add_is_confirmed_tracking(self):
        return OrderTracker.objects.get_or_create(
            order=self,
            status=OrderTrackingStatusChoices.IS_CONFIRMED,
        )

    def add_is_prepared_tracking(self):
        return OrderTracker.objects.get_or_create(
            order=self,
            status=OrderTrackingStatusChoices.IS_PREPARED,
        )

    def add_is_shipped_tracking(self):
        return OrderTracker.objects.get_or_create(
            order=self,
            status=OrderTrackingStatusChoices.IS_SHIPPED,
        )

    def add_is_in_delivered_tracking(self):
        return OrderTracker.objects.get_or_create(
            order=self,
            status=OrderTrackingStatusChoices.IS_DELIVERED,
        )

    def rollback_order_items_inventory(self):
        """Rollback items quantity to inventory"""
        order_items = self.items.all()
        if not order_items:
            return False
        for item in order_items:
            item.rollback_inventory_quantity()
        return True

    def update_order_items_status(self):
        """Update status of order items"""
        items = self.items.all()
        items_status = None
        if self.status == OrderStatusChoices.CONFIRMED:
            items_status = OrderItemStatusChoices.CONFIRMED
        elif self.status == OrderStatusChoices.PAID:
            items_status = OrderItemStatusChoices.PAID
        elif self.status in OrderStatusChoices.fail_status_set():
            items_status = OrderItemStatusChoices.CANCELLED

        if items_status:
            for item in items:
                item.status = items_status
                item.save()

        return True

    def send_order_paid_email(self):

        context = {
            "instance": self,
        }
        try:
            OrderReciptEmail(context=context).send(to=[self.user.email])
        except:
            return False

        return True

    def dispatch_order_tracking(self):
        """Dispatch Order tracking and Send Emails"""
        if self.status == OrderStatusChoices.CONFIRMED:
            self.add_is_confirmed_tracking()

        elif self.status == OrderStatusChoices.PAID:
            if self.payment_type == PaymentTypesChoices.CIA:
                self.send_order_paid_email()

        return True

    @property
    def is_first_order(self):
        return not self.__class__.filter(user=self.user).exclude(id=self.id).exists()
