# Django Imports
from django.db.models.signals import pre_save
from django.dispatch import receiver

# First Party Imports
from base.users.models import Referral
from base.utility.models import AppConfiguration


@receiver(pre_save, sender=Referral)
def referral_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.id:
        if not instance.points:
            instance.points = AppConfiguration.get_referral_points()
