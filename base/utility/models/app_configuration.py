# Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel


class AppConfiguration(AbstractModel):
    """AppConfiguration model"""

    referral_points = models.PositiveIntegerField(
        verbose_name=_("Referral Points"),
        help_text=_("Points to be claimed on referal."),
    )

    class Meta:
        verbose_name = _("App Configuration")
        verbose_name_plural = _("App Configurations")

    def save(self, *args, **kwargs):
        if not self.pk and AppConfiguration.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError("There is be only one AppConfiguration.")
        return super(AppConfiguration, self).save(*args, **kwargs)

    @classmethod
    def get_referral_points(cls):
        points = 0
        app_config = cls.objects.first()
        if app_config:
            points = app_config.referral_points
        return points
