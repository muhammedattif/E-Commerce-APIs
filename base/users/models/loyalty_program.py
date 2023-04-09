# Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import IntegerField, Sum
from django.db.models.functions import Coalesce
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
