# Python Standard Library Imports

# Django Imports
from django.conf import settings
from django.db import models, transaction
from django.db.models import F, FloatField, Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.payment.utils.result_choices import CheckoutResultChoices
from base.utility.utility_models import AbstractModelWithHistory

from .order import Order
from .order_item import OrderItem


class Cart(AbstractModelWithHistory):
    user = models.OneToOneField(
        "base.User",
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name=_("User"),
    )
    total = models.FloatField(
        default=0,
        verbose_name=_("Total"),
    )
    sub_total = models.FloatField(
        default=0,
        verbose_name=_("Sub total"),
    )
    discount = models.FloatField(
        default=0,
        verbose_name=_("Discount"),
    )
    taxes = models.FloatField(
        default=0,
        verbose_name=_("Taxes"),
    )

    class Meta:
        db_table = "payment_carts"
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.id:
            self._recalculate_cart_amount()

    def __str__(self):
        return f"{self.user.email}"

    def _calculate_sub_total(self):
        sub_total = self.items.aggregate(
            sum=Coalesce(
                Sum(F("model__price") * F("quantity")),
                0,
                output_field=FloatField(),
            ),
        )["sum"]
        self.sub_total = round(sub_total, 2)
        return self.sub_total

    def _calculate_discount(self):
        self.discount = 0
        return self.discount

    def _calculate_total(self):
        self.total = self.sub_total - self.discount
        return self.total

    def _calculate_taxes(self):
        self.taxes = round(self.total * (settings.TAX_AMOUNT / 100), 2)
        return self.taxes

    def _recalculate_cart_amount(self):
        self._calculate_sub_total()
        self._calculate_discount()
        self._calculate_total()
        self._calculate_taxes()
        self.save()

    def clear(self):
        self.total = 0
        self.sub_total = 0
        self.discount = 0
        self.taxes = 0
        self.items.all().delete()
        self.save()
        return True

    @transaction.atomic
    def checkout(self, address):
        order = None
        extra_dict = {}

        # Get cart items
        cart_items = self.items.select_related("model", "product")
        if not cart_items:
            return order, CheckoutResultChoices.EMPTY_CART, extra_dict

        # Check if all items quantity available
        # Cart items may be added for a long time
        for item in cart_items:
            if item.model.is_out_of_stock:
                extra_dict = {
                    "product_name": item.product.name,
                }
                return order, CheckoutResultChoices.ITEM_OUT_OF_STOCK, extra_dict

            elif not item.is_available_in_inventory:
                extra_dict = {
                    "product_name": item.product.name,
                    "available_quantity": item.model.inventory_quantity,
                }
                return order, CheckoutResultChoices.ITEM_QUANTITY_UNAVAILABLE, extra_dict

        # Copy Cart Data and Items and create new Order
        order = Order.objects.create(
            user=self.request.user,
            total=self.total,
            sub_total=self.sub_total,
            discount=self.discount,
            taxes=self.taxes,
            address=address,
        )
        for item in cart_items:
            OrderItem.objects.create(
                product=item.product,
                order=order,
                model=item.model,
                price=item.model.price,
                quantity=item.quantity,
            )
        return order, CheckoutResultChoices.SUCCESS, extra_dict
