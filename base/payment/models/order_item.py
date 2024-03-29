# Django Imports
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.payment.utils.choices import OrderItemStatusChoices, OrderStatusChoices
from base.utility.utility_models import AbstractModelWithHistory


class OrderItem(AbstractModelWithHistory):
    order = models.ForeignKey(
        "base.Order",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Order"),
    )
    product = models.ForeignKey(
        "base.Product",
        on_delete=models.RESTRICT,
        verbose_name=_("Product"),
    )
    model = models.ForeignKey(
        "base.Model",
        verbose_name=_("Model"),
        related_name="order_items",
        on_delete=models.RESTRICT,
    )
    price = models.FloatField(
        verbose_name=_("Price"),
    )
    discount = models.FloatField(
        default=0,
        verbose_name=_("Discount"),
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
        verbose_name=_("Quantity"),
    )
    quantity_refunded = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantity Refunded"),
    )

    status = models.IntegerField(
        choices=OrderItemStatusChoices.choices,
        default=OrderItemStatusChoices.INITIATED,
        verbose_name=_("Status"),
    )
    quantity_rolledback_to_inventory = models.BooleanField(
        default=False,
        verbose_name=_("Quantity RolledBack to Inventory"),
    )

    class Meta:
        db_table = "payment_order_items"
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return "{0} | Item: #{1}".format(
            self.order.__str__(),
            self.id,
        )

    def clean_fields(self, **kwargs):

        old_order_item = self.__class__.objects.filter(id=self.id).last()
        if (
            old_order_item
            and old_order_item.status in OrderItemStatusChoices.fail_status_set()
            and self.status in OrderItemStatusChoices.success_status_set()
        ):
            raise ValidationError(
                {
                    "status": _("Order Item reached its final status."),
                },
            )
        super(OrderItem, self).clean_fields(**kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(OrderItem, self).save(*args, **kwargs)

    def subtract_quantity_from_inventory(self, commit=True):

        self.model.inventory_quantity = models.F("inventory_quantity") - self.quantity
        self.model.save()

        self.quantity_rolledback_to_inventory = False
        if commit:
            self.save()

        return True

    def rollback_inventory_quantity(self, quantity=None, commit=True):

        if not quantity:
            quantity = self.quantity

        if self.quantity_rolledback_to_inventory:
            return False

        if self.order.status != OrderStatusChoices.PAID:
            return False

        if self.status != OrderItemStatusChoices.PAID:
            return False

        if quantity > self.quantity:
            return False

        self.model.inventory_quantity = models.F("inventory_quantity") + quantity
        self.model.save()

        self.quantity_rolledback_to_inventory = True
        if commit:
            self.save()
        return True
