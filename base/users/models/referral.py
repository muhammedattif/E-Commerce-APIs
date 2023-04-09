# Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel


class Referral(AbstractModel):
    """
    Referral model
    """

    loyalty_program = models.ForeignKey(
        "base.LoyaltyProgram",
        on_delete=models.CASCADE,
        related_name="referrals",
        verbose_name=_("Loyalty Program"),
    )

    referent = models.OneToOneField(
        "base.User",
        on_delete=models.CASCADE,
        related_name="referral",
        verbose_name=_("Referent"),
    )

    points = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Points"),
        help_text=_("Points Claimed"),
    )
    is_first_item_purchased = models.BooleanField(
        default=False,
        verbose_name=_("Is First Item Purchased?"),
    )

    class Meta:
        db_table = "users_referrals"
        verbose_name = _("Referral")
        verbose_name_plural = _("Referrals")

    def __str__(self):
        return "{0} | Awarded {1}".format(
            self.referent.email,
            self.points,
        )

    def clean_fields(self, **kwargs) -> None:
        super().clean_fields(**kwargs)

        if self.loyalty_program.referrer == self.referent:
            raise ValidationError(_("Referrer cannot be referred."))
