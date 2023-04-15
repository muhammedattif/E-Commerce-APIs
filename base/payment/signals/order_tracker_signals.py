# Django Imports
from django.db.models.signals import post_save
from django.dispatch import receiver

# First Party Imports
from base.payment.models import OrderTracker


@receiver(post_save, sender=OrderTracker)
def order_tracker_post_save_signal(sender, instance, created, *args, **kwargs):
    if created:
        instance.send_tracking_email()
