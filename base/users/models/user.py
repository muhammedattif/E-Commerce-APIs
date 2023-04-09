# Python Standard Library Imports
from smtplib import SMTPException

# Django Imports
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import IntegerField, Sum
from django.db.models.functions import Coalesce
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

# REST Framework Imports
from rest_framework.authtoken.models import Token

# First Party Imports
from base.users.emails import ActivationEmail, ConfirmationEmail
from base.users.fields import LowercaseEmailField
from base.users.managers import UserManager
from base.utility.utility_models import AbstractModel

from .loyalty_program import LoyaltyProgram
from .referral import Referral


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    """User Model"""

    class GenderTypes(models.IntegerChoices):
        MALE = 0, _("Male")
        FEMALE = 1, _("Female")

    # Basic Info
    email = LowercaseEmailField(
        max_length=60,
        unique=True,
        verbose_name=_("Email"),
    )
    first_name = models.CharField(null=True, max_length=30, verbose_name=_("First name"))
    last_name = models.CharField(null=True, max_length=30, verbose_name=_("Last Name"))
    gender = models.IntegerField(null=True, choices=GenderTypes.choices, verbose_name=_("Gender"))

    # Dates
    last_login = models.DateTimeField(auto_now=True, verbose_name=_("Last Login"))
    last_logout = models.DateTimeField(blank=True, null=True, verbose_name=_("Last Logout"))
    last_action = models.DateTimeField(blank=True, null=True, verbose_name=_("Last Action"))
    birth_date = models.DateField(null=True, verbose_name=_("Birth Date"))

    # Bool Flags
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))
    is_guest = models.BooleanField(default=False, verbose_name=_("Is Guest"))
    is_seller = models.BooleanField(default=False, verbose_name=_("Is Seller"))
    is_buyer = models.BooleanField(default=True, verbose_name=_("Is Buyer"))
    is_suspended = models.BooleanField(default=False, verbose_name=_("Is Suspended"))
    is_email_verified = models.BooleanField(default=False, verbose_name=_("Is Email Verified"))
    is_online = models.BooleanField(default=False, verbose_name=_("Online"))

    # Addons
    referral_code = models.CharField(max_length=20, verbose_name=_("Referral Code"))

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    objects = UserManager()

    def unsuspend(self, commit=True):
        if self.is_suspended:
            self.is_suspended = False
            self.is_active = True
            if commit:
                self.save()
        return True

    def suspend(self):
        if not self.is_suspended:
            self.is_suspended = True
            self.save()
        return True

    @staticmethod
    def encode_uid(pk):
        return force_str(urlsafe_base64_encode(force_bytes(pk)))

    @staticmethod
    def decode_uid(pk):
        return force_str(urlsafe_base64_decode(pk))

    def send_activation_email(self):
        """send activation email"""
        if self.is_active:
            return False

        context = {
            "user": self,
        }
        try:
            ActivationEmail(context=context).send(to=[self])
        except SMTPException:
            return False
        return True

    def send_confirmation_email(self):
        """send confirmation email"""

        if not self.is_active:
            return False

        context = {
            "user": self,
        }
        try:
            ConfirmationEmail(context=context).send(to=[self])
        except SMTPException:
            return False
        return True

    def generate_new_token(self):
        self.delete_previous_tokens()
        return Token.objects.create(user=self)

    def get_total_referral_points(self):
        return self.loyalty_program.referrals.filter(is_active=True).aggregate(
            sum=Coalesce(
                Sum("points"),
                0,
                output_field=IntegerField(),
            ),
        )["sum"]

    def get_not_claimed_referral_points(self):
        claimed_points = self.loyalty_program.claimed_points
        points_to_be_claimed = self.loyalty_program.referrals.filter(
            is_first_item_purchased=True,
            is_active=True,
        ).aggregate(
            sum=Coalesce(
                Sum("points"),
                0,
                output_field=IntegerField(),
            ),
        )[
            "sum"
        ]
        return points_to_be_claimed - claimed_points

    def record_referral(self, referral_code):
        if not referral_code:
            return False

        referrer = User.objects.filter(referral_code=referral_code)
        loyalty_program, created = LoyaltyProgram.objects.get_or_create(
            referrer=referrer,
        )
        Referral.objects.create(
            loyalty_program=loyalty_program,
            referent=self,
        )
        return True
