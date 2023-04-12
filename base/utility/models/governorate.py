# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel


class Governorate(AbstractModel):
    """Governorate model"""

    en_name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("English Name"),
    )
    ar_name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Arabic Name"),
    )

    class Meta:
        db_table = "utility_governorates"
        verbose_name = _("Governorate")
        verbose_name_plural = _("Governorates")

    def __str__(self):
        return "{0}".format(self.ar_name)
