# Django Imports
from django.db import models


class InventoryStatuses(models.IntegerChoices):
    OUT_OF_STOCK = 0, ("Out of Stock")
    AVAILABLE = 1, ("Available")
    QUANTITY_UNAVAILBLE = 2, ("Quantity Unavailable")
    NOT_AVAILBLE = 3, ("Not Available")
