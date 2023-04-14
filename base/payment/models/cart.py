# Python Standard Library Imports

# Django Imports
from django.conf import settings
from django.db import models
from django.db.models import F, FloatField, Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility.utility_models import AbstractModelWithHistory


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
