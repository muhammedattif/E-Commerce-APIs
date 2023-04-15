# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderTrackingStatusChoices(models.IntegerChoices):
    IS_CONFIRMED = 0, _("Is Confirmed")
    IS_PREPARED = 1, _("Is Prepared")
    IS_SHIPPED = 2, _("Is Shipped")
    IS_DELIVERED = 3, _("Is Delivered")
