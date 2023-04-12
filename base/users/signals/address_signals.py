# Django Imports
from django.db.models.signals import post_save
from django.dispatch import receiver

# First Party Imports
from base.users.models import Address


@receiver(post_save, sender=Address)
def address_postsave_signal(sender, instance, created, *args, **kwargs):
    if created:
        instance.process_primary()
