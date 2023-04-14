# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel


class Model(AbstractModel):

    product = models.ForeignKey(
        "base.Product",
        on_delete=models.CASCADE,
        related_name="models",
        verbose_name=_("Product"),
    )
    product_options = models.ManyToManyField(
        "base.ProductOption",
        verbose_name=_("Product Options"),
    )
    inventory_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Inventory Quantity"),
    )
    price = models.FloatField(verbose_name="Price")

    class Meta:
        db_table = "products_models"
        verbose_name = _("Model")
        verbose_name_plural = _("Models")

    def __str__(self) -> str:
        text = self.as_text
        if text:
            return "{0}| {1}".format(self.product.name, text)
        return self.product.name

    @property
    def as_text(self):
        text = ""
        product_options = self.product_options.all()
        if not product_options:
            return text
        for option in product_options:
            text += "{0}: {1} ".format(
                option.product_feature.name,
                option.name,
            )
        return text
