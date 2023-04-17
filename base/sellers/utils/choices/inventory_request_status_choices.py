# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class InventoryRequestStatusChoices(models.IntegerChoices):
    SUBMITTED = 0, _("Submitted")
    APPROVED = 6, _("Approved")
    DECLINED = 7, _("Declined")
