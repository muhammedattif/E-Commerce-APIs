# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility.utility_models import AbstractModel


class SysFeature(AbstractModel):

    name = models.CharField(max_length=100, verbose_name=_("Name"))

    class Meta:
        db_table = "products_sys_features"
        verbose_name = _("System Features")
        verbose_name_plural = _("System Features")

    def __str__(self):
        return self.name
