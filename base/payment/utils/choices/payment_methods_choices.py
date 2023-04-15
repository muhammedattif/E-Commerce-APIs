# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentMethodsChoices(models.IntegerChoices):
    CREDIT_CARD = 0, _("Credit Card")
    APPLE_PAY = 1, _("Apple Pay")
    PAY_BY_INSTALMENTS = 2, _("Pay By Instalments")
