# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class CheckoutResultChoices(models.IntegerChoices):
    EMPTY_CART = 0, _("Cart Is  Empty")
    ITEM_OUT_OF_STOCK = 1, _("Item out of Stock")
    ITEM_QUANTITY_UNAVAILABLE = 2, _("Item Quantity Unavailable")
    SUCCESS = 3, _("Checkout Successfully")
