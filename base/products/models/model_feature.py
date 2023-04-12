# Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility.utility_models import AbstractModel

from .sys_feature import SysFeature


class ModelFeature(AbstractModel):

    model = models.ForeignKey(
        "base.Model",
        verbose_name=_("Model"),
        on_delete=models.CASCADE,
        related_name="features",
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    class Meta:
        db_table = "products_model_features"
        verbose_name = _("Model Features")
        verbose_name_plural = _("Model Features")

    def __str__(self):
        return self.name

    def clean_fields(self, **kwargs) -> None:
        super().clean_fields(**kwargs)

        if not SysFeature.objects.filter(name=self.name, is_active=True).exists():
            raise ValidationError(
                {
                    "name": _("Invalid Name. This Name must be pre-defined in System Features."),
                },
            )
