# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility.utility_models import AbstractModel, AbstractTracker


class CategoryTracker(AbstractModel, AbstractTracker):

    category = models.ForeignKey(
        "base.Category",
        on_delete=models.CASCADE,
        related_name="trackers",
        verbose_name=_("Category"),
    )

    class Meta:
        db_table = "utility_category_trackers"
        verbose_name = _("Category Tracker")
        verbose_name_plural = _("Category Trackers")

    def __str__(self):
        return f"User:{self.user}-Category:{self.category.name}-Views:{self.views}"
