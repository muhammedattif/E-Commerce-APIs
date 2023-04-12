# Django Imports
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# REST Framework Imports
from rest_framework.authtoken.models import Token

# First Party Imports
from base.users.models import Favorite, LoyaltyProgram, User
from base.utility.random import generate_random_referal_code


@receiver(pre_save, sender=User)
def user_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.referral_code = generate_random_referal_code()


@receiver(post_save, sender=User)
def user_post_save_signal(instance, created, *args, **kwargs):
    if created:
        # Create User Token
        Token.objects.create(user=instance)

        # Create Loyalty Program
        LoyaltyProgram.objects.create(referrer=instance)

        # Create Favorite
        Favorite.objects.create(user=instance)

        # Send Activation Email
        if settings.SEND_ACTIVATION_EMAIL and not instance.is_active:
            instance.send_activation_email()
