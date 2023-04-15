# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class InventoryRequestStatusChoices(models.IntegerChoices):
    SUBMITTED = 0, _("Submitted")
    ALREADY_APPROVED = 1, _("Already Approved")
    ALREADY_DECLINED = 2, _("Already Declined")
    QUANTITY_UNAVAILBLE = 3, _("Quantity Unavailable")
    CANNOT_APPROVE = 4, _("Cannot be Approved")
    CANNOT_DECLINE = 5, _("Cannot be Declined")
    APPROVED = 6, _("Approved")
    DECLINED = 7, _("Declined")
