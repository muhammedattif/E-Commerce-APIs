# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel


class City(AbstractModel):
    """City model"""

    en_name = models.CharField(
        max_length=50,
        verbose_name=_("English Name"),
    )
    ar_name = models.CharField(
        max_length=50,
        verbose_name=_("Arabic Name"),
    )
    governorate = models.ForeignKey(
        "base.Governorate",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "utility_cities"
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        constraints = [
            models.UniqueConstraint(fields=["en_name", "ar_name", "governorate"], name="unique city"),
        ]

    def __str__(self):
        return "{0}".format(self.ar_name)
