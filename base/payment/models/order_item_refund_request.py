# Python Standard Library Imports
from datetime import datetime

# Django Imports
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.payment.emails import ItemRefundedEmail, ItemRefundRequestEmail
from base.payment.utils.choices import OrderItemStatusChoices
from base.utility.choices import ApprovalActionChoices
from base.utility.utility_models import AbstractModelWithHistory


class OrderItemRefundRequest(AbstractModelWithHistory):
    status = models.IntegerField(
        choices=ApprovalActionChoices.choices,
        default=ApprovalActionChoices.SUBMITTED,
        verbose_name=_("Status"),
    )
    item = models.ForeignKey(
        "base.OrderItem",
        verbose_name=_("Order Item"),
        on_delete=models.CASCADE,
    )
    additional_info = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Additional Info"),
    )
    quantity = models.PositiveIntegerField(
        blank=False,
        default=1,
        validators=[
            MinValueValidator(1),
        ],
        verbose_name=_("Quantity"),
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
        db_table = "payment_order_item_refund_requests"
        verbose_name = _("Order Item Refund Request")
        verbose_name_plural = _("Order Item Refund Requests")

    def __str__(self):
        return f"Item| {self.item.product.name} - Order #{self.item.order.id}"

    @transaction.atomic
    def approve(self, action_user):
        """
        Approve Refund Request
        1- Refund Item (Return Quantity to inventory)
        2- Update request status
        """

        if self.status != ApprovalActionChoices.SUBMITTED:
            return False

        is_refunded = self.item.rollback_inventory_quantity(quantity=self.quantity)
        if not is_refunded:
            return False

        self.item.status = OrderItemStatusChoices.REFUNDED
        self.item.quantity_refunded = self.quantity
        self.item.save()

        self.status = ApprovalActionChoices.APPROVED
        self.action_taken_at = datetime.now()
        self.action_taken_by = action_user
        self.save()
        return True

    def decline(self, action_user):
        """
        Decline Refund Request
        1- Update request status
        """

        if self.status != ApprovalActionChoices.SUBMITTED:
            return False
        self.status = ApprovalActionChoices.DECLINED
        self.action_taken_at = datetime.now()
        self.action_taken_by = action_user
        self.save()
        return True

    def send_request_submitted_email_to_admin_and_vendor(self):
        # Send email to the Admin and the Vendor
        emails_list = [self.item.product.seller.email]
        context = {
            "instance": self,
        }
        try:
            ItemRefundRequestEmail(context=context).send(to=emails_list)
        except:
            return False

        return True

    def send_approval_email_to_user(self):
        context = {
            "instance": self,
        }
        try:
            ItemRefundedEmail(context=context).send(to=[self.item.order.user.email])
        except:
            return False
        return True

    def send_decline_email_to_user(self):
        pass

    def send_refund_status_email_to_user(self):
        """send refund request status email to the user"""

        if self.status == ApprovalActionChoices.APPROVED:
            self.send_approval_email_to_user()

        elif self.status == ApprovalActionChoices.DECLINED:
            self.send_decline_email_to_user()

        return True
