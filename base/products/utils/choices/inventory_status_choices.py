# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class InventoryStatusChoices(models.IntegerChoices):
    OUT_OF_STOCK = 0, _("Out of Stock")
    AVAILABLE = 1, _("Available")
    QUANTITY_UNAVAILBLE = 2, _("Quantity Unavailable")
    NOT_AVAILBLE = 3, _("Not Available")
