# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility.utility_models import AbstractModel, AbstractTracker


class BrandTracker(AbstractModel, AbstractTracker):

    brand = models.ForeignKey("base.Brand", on_delete=models.CASCADE, related_name="trackers", verbose_name=_("Brand"))

    class Meta:
        db_table = "utility_brand_trackers"
        verbose_name = _("Brand Tracker")
        verbose_name_plural = _("Brand Trackers")

    def __str__(self):
        return f"User:{self.user}-Brand:{self.brand.name}-Views:{self.views}"
