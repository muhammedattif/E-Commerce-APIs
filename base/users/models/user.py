# Python Standard Library Imports
from smtplib import SMTPException

# Django Imports
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.users.emails import ActivationEmail, ConfirmationEmail
from base.users.fields import LowercaseEmailField, LowercaseUsernameField
from base.users.managers import UserManager
from base.users.validators import ASCIIUsernameValidator
from base.utility.utility_models import AbstractModel


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
    username = LowercaseUsernameField(
        max_length=30,
        unique=True,
        validators=[ASCIIUsernameValidator()],
        verbose_name=_("Username"),
    )
    first_name = models.CharField(max_length=30, verbose_name=_("First name"))
    last_name = models.CharField(max_length=30, verbose_name=_("Last Name"))
    gender = models.IntegerField(choices=GenderTypes.choices, verbose_name=_("Gender"))

    # Dates
    last_login = models.DateTimeField(auto_now=True, verbose_name=_("Last Login"))
    last_logout = models.DateTimeField(blank=True, null=True, verbose_name=_("Last Logout"))
    last_action = models.DateTimeField(blank=True, null=True, verbose_name=_("Last Action"))
    birth_date = models.DateTimeField(verbose_name=_("Birth Date"))

    # Bool Flags
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))
    is_guest = models.BooleanField(default=False, verbose_name=_("Is Guest"))
    is_suspended = models.BooleanField(default=False, verbose_name=_("Is Suspended"))
    is_email_verified = models.BooleanField(default=False, verbose_name=_("Is Email Verified"))
    is_online = models.BooleanField(default=False, verbose_name=_("Online"))

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

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
