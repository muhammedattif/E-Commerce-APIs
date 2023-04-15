# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatusChoices(models.IntegerChoices):
    INITIATED = 0, _("Initiated")
    CONFIRMED = 1, _("Confirmed")
    CANCELLED = 2, _("Cancelled")
    EXPIRED = 3, _("Expired")
    FAILED = 4, _("Failed")
    PAID = 5, _("Paid")

    @classmethod
    def success_status_set(cls):
        return [
            cls.INITIATED,
            cls.CONFIRMED,
            cls.PAID,
        ]

    @classmethod
    def fail_status_set(cls):
        return [
            cls.CANCELLED,
            cls.EXPIRED,
            cls.FAILED,
        ]
