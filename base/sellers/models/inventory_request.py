# Python Standard Library Imports
from datetime import datetime

# Django Imports
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel


class InventoryRequest(AbstractModel):

    seller = models.ForeignKey(
        "base.User",
        on_delete=models.PROTECT,
        related_name="invenrory_requests",
        verbose_name=_("Seller"),
    )
    model = models.ForeignKey(
        "base.Model",
        on_delete=models.PROTECT,
        verbose_name=_("Model"),
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Quantity"),
    )
    is_approved = models.BooleanField(default=False, verbose_name=_("Is Approved?"))
    approved_by = models.ForeignKey(
        "base.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Approved By"),
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Approved At"),
    )

    class Meta:
        db_table = "products_inventory_requests"
        verbose_name = _("Inventory Request")
        verbose_name_plural = _("Inventory Requests")

    def __str__(self) -> str:
        return "{0} | {1}".format(
            self.seller.email,
            self.model.__str__(),
        )

    def clean_fields(self, **kwargs) -> None:
        super().clean_fields(**kwargs)
        if self.seller != self.model.product.seller:
            raise ValidationError(_("Model {0} is not related to seller {1}").format(self.model, self.seller))

    def approve(self, user):
        """
        Approve Inventory Request:
        1- Update Model Inventory Quantity
        2- Update Approved At and Approved By
        3- Mark Request as Approved
        """
        if self.is_approved:
            return False

        self.model.inventory_quantity += models.F("inventory_quantity") + self.quantity
        self.model.save()

        self.approved_at = datetime.now()
        self.approved_by = user
        self.is_approved = True
        self.save()

        return True
