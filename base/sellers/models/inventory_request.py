# Python Standard Library Imports
from datetime import datetime

# Django Imports
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.sellers.utils.choices import InventoryRequestStatusChoices, InventoryRequestTypesChoices
from base.utility import AbstractModel


class InventoryRequest(AbstractModel):

    seller = models.ForeignKey(
        "base.User",
        on_delete=models.PROTECT,
        related_name="invenrory_requests",
        verbose_name=_("Seller"),
    )
    type = models.IntegerField(
        choices=InventoryRequestTypesChoices.choices,
        verbose_name=_("Type"),
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
    status = models.IntegerField(
        choices=InventoryRequestStatusChoices.choices,
        verbose_name=_("Status"),
    )
    action_taken_by = models.ForeignKey(
        "base.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Action Taken By"),
    )
    action_taken_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Action Taken At"),
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

    def approve(self, action_user):
        """
        Approve Inventory Request:
        1- Update Model Inventory Quantity
        2- Update Approved At and Approved By
        3- Mark Request as Approved
        """
        if self.status == InventoryRequestStatusChoices.APPROVED:
            return False, InventoryRequestStatusChoices.ALREADY_APPROVED

        if self.status == InventoryRequestStatusChoices.DECLINED:
            return False, InventoryRequestStatusChoices.ALREADY_DECLINED

        if self.status != InventoryRequestStatusChoices.SUBMITTED:
            return False, InventoryRequestStatusChoices.CANNOT_DECLINE

        if self.type == InventoryRequestTypesChoices.ADD:
            self.model.inventory_quantity += models.F("inventory_quantity") + self.quantity
        elif self.type == InventoryRequestTypesChoices.RETURN:
            if not self.model.is_available_in_inventory(quantity=self.quantity):
                return False, InventoryRequestStatusChoices.QUANTITY_UNAVAILBLE
            self.model.inventory_quantity += models.F("inventory_quantity") - self.quantity

        self.model.save()

        self.action_taken_at = datetime.now()
        self.action_taken_by = action_user
        self.status = InventoryRequestStatusChoices.APPROVED
        self.save()

        return True, InventoryRequestStatusChoices.APPROVED

    def decline(self, action_user):
        """
        Decline Inventory Request:
        """
        if self.status == InventoryRequestStatusChoices.APPROVED:
            return False, InventoryRequestStatusChoices.ALREADY_APPROVED

        if self.status == InventoryRequestStatusChoices.DECLINED:
            return False, InventoryRequestStatusChoices.ALREADY_DECLINED

        if self.status != InventoryRequestStatusChoices.SUBMITTED:
            return False, InventoryRequestStatusChoices.CANNOT_DECLINE

        self.action_taken_at = datetime.now()
        self.action_taken_by = action_user
        self.status = InventoryRequestStatusChoices.DECLINED
        self.save()

        return True, InventoryRequestStatusChoices.DECLINED
