# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractModel(models.Model):
    """abstract model that is an entry point for common changes across all models"""

    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        abstract = True
