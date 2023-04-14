# Django Imports
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility.utility_models import AbstractModelWithHistory


class CartItem(AbstractModelWithHistory):
    product = models.ForeignKey(
        "base.Product",
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
    )
    cart = models.ForeignKey(
        "base.Cart",
        verbose_name=_("Cart"),
        on_delete=models.CASCADE,
        related_name="items",
    )
    model = models.ForeignKey(
        "base.Model",
        verbose_name=_("Model"),
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
        verbose_name=_("Quantity"),
    )

    class Meta:
        db_table = "payment_cart_items"
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def __str__(self):
        return "{0}".format(self.model.__str__())

    def clean_fields(self, **kwargs) -> None:
        super().clean_fields(**kwargs)

        if self.model.product != self.product:
            raise ValidationError(_("Model: {0} is not related to Product: {1}").format(self.model, self.product))

        if self.model.is_out_of_stock:
            raise ValidationError(_("Model: {0} is out of Stock").format(self.model))

        if not self.model.is_available_in_inventory(quantity=self.quantity):
            raise ValidationError(
                _("Model: {0} has only {1} items in Stock").format(self.model, self.model.inventory_quantity),
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.model.price * self.quantity
