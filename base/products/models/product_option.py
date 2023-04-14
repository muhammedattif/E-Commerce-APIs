# Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility.utility_models import AbstractModel

from .sys_option import SysOption


class ProductOption(AbstractModel):

    product_feature = models.ForeignKey(
        "base.ProductFeature",
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("Product Feature"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    class Meta:
        db_table = "products_product_options"
        verbose_name = _("Product Options")
        verbose_name_plural = _("Product Options")

    def __str__(self):
        return "{0}| {1}: {2}".format(
            self.id,
            self.product_feature.name,
            self.name,
        )

    def clean_fields(self, **kwargs) -> None:
        super().clean_fields(**kwargs)

        if not SysOption.objects.filter(
            name=self.name,
            is_active=True,
            sys_feature__name=self.product_feature.name,
            sys_feature__is_active=True,
        ).exists():
            raise ValidationError(
                {
                    "name": _("Invalid Name. This Name must be pre-defined in System Options."),
                },
            )
