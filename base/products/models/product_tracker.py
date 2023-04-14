# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility.utility_models import AbstractModel, AbstractTracker


class ProductTracker(AbstractModel, AbstractTracker):

    product = models.ForeignKey(
        "base.Product",
        on_delete=models.CASCADE,
        related_name="trackers",
        verbose_name=_("Product"),
    )

    class Meta:
        db_table = "utility_product_trackers"
        verbose_name = _("Product Tracker")
        verbose_name_plural = _("Product Trackers")

    def __str__(self):
        return f"User:{self.user}-Product:{self.brand.name}-Views:{self.views}"
