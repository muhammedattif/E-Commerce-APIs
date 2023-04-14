# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Other Third Party Imports
from simple_history.models import HistoricalRecords

# First Party Imports
from base.utility.functions.simple_history import adjusted_get_user


class AbstractModel(models.Model):
    """abstract model that is an entry point for common changes across all models"""

    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True


class AbstractModelWithHistory(AbstractModel):
    """abstract model with history"""

    history = HistoricalRecords(get_user=adjusted_get_user, verbose_name=_("History"), inherit=True)

    class Meta:
        abstract = True
