# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.payment.emails import OrderConfirmedEmail
from base.payment.utils.choices import OrderTrackingStatusChoices
from base.utility.utility_models import AbstractModelWithHistory


class OrderTracker(AbstractModelWithHistory):

    order = models.ForeignKey(
        "base.Order",
        on_delete=models.CASCADE,
        related_name="tracker",
    )
    status = models.IntegerField(
        choices=OrderTrackingStatusChoices.choices,
        verbose_name=_("Status"),
    )
    additional_info = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Additional info"),
    )
    estimated_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Estimated Date"),
    )

    def __str__(self):
        return f"{self.order}-{self.status}"

    def send_order_confirmed_email(self):
        context = {
            "instance": self,
        }
        try:
            OrderConfirmedEmail(context=context).send(to=[self.user.email])
        except:
            return False

        return True

    def send_order_prepared_email(self):
        pass

    def send_order_shipped_email(self):
        pass

    def send_order_delivered_email(self):
        pass

    def send_tracking_email(self):
        """send tracking email based on tracking status"""

        if self.status == OrderTrackingStatusChoices.IS_CONFIRMED:
            self.send_order_confirmed_email()
        elif self.status == OrderTrackingStatusChoices.IS_PREPARED:
            self.send_order_prepared_email()
        elif self.status == OrderTrackingStatusChoices.IS_SHIPPED:
            self.send_order_prepared_email()
        elif self.status == OrderTrackingStatusChoices.IS_DELIVERED:
            self.send_order_delivered_email()

        return True
