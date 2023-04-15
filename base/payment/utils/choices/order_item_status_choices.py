# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderItemStatusChoices(models.IntegerChoices):
    INITIATED = 0, _("Initiated")
    CONFIRMED = 1, _("Confirmed")
    RETURNED = 2, _("Returned")
    REFUNDED = 3, _("Refunded")
    CANCELLED = 4, _("Cancelled")
    PAID = 5, _("Paid")

    @classmethod
    def success_status_set(cls):
        return [
            cls.INITIATED,
            cls.PAID,
        ]

    @classmethod
    def fail_status_set(cls):
        return [
            cls.RETURNED,
            cls.CANCELLED,
            cls.REFUNDED,
        ]
