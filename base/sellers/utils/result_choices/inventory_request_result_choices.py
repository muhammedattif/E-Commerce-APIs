# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class InventoryRequestResultChoices(models.IntegerChoices):
    ALREADY_APPROVED = 0, _("Already Approved")
    ALREADY_DECLINED = 1, _("Already Declined")
    QUANTITY_UNAVAILBLE = 2, _("Quantity Unavailable")
    CANNOT_APPROVE = 3, _("Cannot be Approved")
    CANNOT_DECLINE = 4, _("Cannot be Declined")
    APPROVED = 5, _("Approved")
    DECLINED = 6, _("Declined")
