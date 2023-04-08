# Django Imports
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# REST Framework Imports
from rest_framework.authtoken.models import Token

# First Party Imports
from base.users.models import User


@receiver(post_save, sender=User)
def user_post_signal(instance, created, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)

        if settings.SEND_ACTIVATION_EMAIL and not instance.is_active:
            instance.send_activation_email()
