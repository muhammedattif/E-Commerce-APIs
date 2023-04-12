# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility.utility_models import AbstractModel


class SysOption(AbstractModel):

    sys_feature = models.ForeignKey(
        "base.SysFeature",
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("System Feature"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    class Meta:
        db_table = "products_sys_options"
        verbose_name = _("System Options")
        verbose_name_plural = _("System Options")

    def __str__(self):
        return self.name
