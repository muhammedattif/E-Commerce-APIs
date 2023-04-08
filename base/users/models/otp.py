# Python Standard Library Imports
import string
from datetime import datetime, timedelta

# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel, generate_random


class OTP(AbstractModel):
    """
    One Time Pin model
    """

    class OTPTypes(models.IntegerChoices):
        RESET_PASSWORD = 0, _("Reset Password")
        EMAIL_VERIFICATION = 1, _("Email Verification")

    user = models.ForeignKey(
        "base.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_("Email"),
    )
    otp_type = models.IntegerField(choices=OTPTypes.choices, verbose_name=_("OTP Type"))
    pin = models.CharField(max_length=10, db_index=True, verbose_name=_("OTP"))

    secret_token = models.ForeignKey(
        "base.SecretToken",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Secret Token"),
    )
    expires_at = models.DateTimeField(null=False, verbose_name=_("Expires At"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        db_table = "users_one_time_pin"
        verbose_name = _("One Time Pin")
        verbose_name_plural = _("One Time Pins")

    def __str__(self):
        return self.pin

    def save(self, *args, **kwargs):
        if not self.pin:
            self.pin = self.generate_pin()
        return super(OTP, self).save(*args, **kwargs)

    @staticmethod
    def generate_pin(otp_length=6):
        """generates pin of any length"""
        return generate_random(size=otp_length, chars=string.digits)

    def deactivate(self):
        self.is_active = False
        self.save()
        return True

    def deactivate_previous_otps(self):

        self.__class__.objects.filter(user=self.user, email=self.email, otp_type=self.otp_type).exclude(
            id=self.id,
        ).update(
            is_active=False,
        )
        return True

    @property
    def masked_pin(self):
        value = None
        if self.pin:
            value = "{0}****{1}".format(self.pin[0], self.pin[-1])
        return value

    @classmethod
    def create(cls, otp_type, user=None, email=None, expiry_seconds=300):  # 5 Min
        """creates one time pin for user"""

        if not (user or email):
            return None

        if otp_type not in cls.OTPTypes:
            return None

        if not isinstance(expiry_seconds, int):
            return None

        expiry_time = datetime.now() + timedelta(seconds=expiry_seconds)
        created_otp = cls.objects.create(
            user=user,
            email=email,
            otp_type=otp_type,
            expires_at=expiry_time,
        )
        return created_otp
