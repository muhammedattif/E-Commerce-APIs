# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel, AbstractModelWithApproval, AbstractModelWithHistory


class AbstractModel(AbstractModel):

    product = models.ForeignKey(
        "base.Product",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
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
        abstract = True

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


class Model(AbstractModel, AbstractModelWithHistory):
    class Meta:
        db_table = "products_models"
        verbose_name = _("Model")
        verbose_name_plural = _("Models")

    @property
    def is_out_of_stock(self):
        return self.inventory_quantity == 0

    def is_available_in_inventory(self, quantity):
        return self.inventory_quantity >= quantity


class ModelApproval(AbstractModel, AbstractModelWithApproval):

    PRIMARY_CLASS = Model
    APPROVAL_FIELDS = [
        "product_options",
        "price",
    ]
    NON_EDITABLE_FIELDS = [
        "id",
        "product",
        "inventory_quantity",
        "created_at",
        "updated_at",
    ]

    product_approval = models.ForeignKey(
        "base.ProductApproval",
        on_delete=models.CASCADE,
        verbose_name=_("Product Approval"),
    )

    class Meta:
        db_table = "products_model_approvals"
        verbose_name = _("Model Approval")
        verbose_name_plural = _("Model Approvals")
