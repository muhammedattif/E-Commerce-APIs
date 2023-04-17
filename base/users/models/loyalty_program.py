# Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import IntegerField, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel


class LoyaltyProgram(AbstractModel):
    """
    Loyalty Program model
    """

    referrer = models.OneToOneField(
        "base.User",
        on_delete=models.CASCADE,
        related_name="loyalty_program",
        verbose_name=_("Referrer"),
    )
    claimed_points = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Claimed Points"),
    )
    used_points = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Used Points"),
    )

    class Meta:
        db_table = "users_loyalty_programs"
        verbose_name = _("Loyalty Program")
        verbose_name_plural = _("Loyalty Programs")

    def __str__(self):
        return "{0} | Claimed {1} Point(s)".format(
            self.referrer.email,
            self.claimed_points,
        )

    def clean_fields(self, **kwargs) -> None:
        super().clean_fields(**kwargs)

        all_points = self.referrals.aggregate(
            sum=Coalesce(
                Sum("points"),
                0,
                output_field=IntegerField(),
            ),
        )["sum"]
        if self.claimed_points > all_points:
            raise ValidationError(_("Claimed Points must not exceed the total points awarded."))

        if self.used_points > self.claimed_points:
            raise ValidationError(_("Used Points must not exceed the total Claimed Points."))

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_total_referral_points(self):
        return self.referrals.filter(is_active=True).aggregate(
            sum=Coalesce(
                Sum("points"),
                0,
                output_field=IntegerField(),
            ),
        )["sum"]

    def get_pending_referral_points(self):
        pending_points = self.referrals.filter(is_claimed=False, is_active=True).aggregate(
            sum=Coalesce(
                Sum("points"),
                0,
                output_field=IntegerField(),
            ),
        )["sum"]
        return pending_points

    def record_referral(self):
        from .referral import Referral

        Referral.objects.create(
            loyalty_program=self,
            referent=self,
        )
        return True

    @classmethod
    def reward_pending_referral_points(cls, order):
        # First Party Imports
        from base.payment.utils.choices import OrderStatusChoices

        if order.status != OrderStatusChoices.PAID:
            return False

        if not order.is_first_order:
            return False

        referent = order.user
        referral_instance = referent.referral_instance
        if referral_instance.is_claimed:
            return False

        referral_instance.is_claimed = True
        referral_instance.claimed_at = timezone.now()
        referral_instance.save()
        return True
