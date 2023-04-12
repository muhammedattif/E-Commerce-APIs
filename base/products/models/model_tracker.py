# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility.utility_models import AbstractModel, AbstractTracker


class ModelTracker(AbstractModel, AbstractTracker):

    model = models.ForeignKey("base.Model", on_delete=models.CASCADE, related_name="trackers", verbose_name=_("Brand"))

    class Meta:
        db_table = "utility_model_trackers"
        verbose_name = _("Model Tracker")
        verbose_name_plural = _("Model Trackers")

    def __str__(self):
        return f"User:{self.user}-Model:{self.brand.name}-Views:{self.views}"
