# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentTypesChoices(models.IntegerChoices):
    CIA = 0, _("Cash In Advance")
    COD = 1, _("Cash On Delivery")
