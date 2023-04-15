# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class InventoryRequestTypesChoices(models.IntegerChoices):
    ADD = 0, _("Add")
    RETURN = 1, _("Return")
