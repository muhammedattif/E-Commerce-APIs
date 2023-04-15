# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class InventoryRequestStatusChoices(models.IntegerChoices):
    ALREADY_APPROVED = 0, _("Already Approved")
    QUANTITY_UNAVAILBLE = 1, _("Quantity Unavailable")
    CANNOT_APPROVE = 2, _("Cannot be Approved")
    APPROVED = 3, _("Approved")
