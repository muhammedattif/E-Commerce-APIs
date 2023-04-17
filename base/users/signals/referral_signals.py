# Django Imports
from django.db.models.signals import post_save
from django.dispatch import receiver

# First Party Imports
from base.users.models import Referral


@receiver(post_save, sender=Referral)
def referral_post_save_signal(sender, instance, created, *args, **kwargs):
    if created:
        if not instance.points:
            instance.set_points()

    if instance.is_claimed:
        instance.update_loyalty_program_claimed_points()
