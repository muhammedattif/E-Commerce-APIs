# Django Imports
from django.db.models.signals import post_save
from django.dispatch import receiver

# First Party Imports
from base.sellers.models import InventoryRequest


@receiver(post_save, sender=InventoryRequest)
def inventory_request_post_save_signal(sender, instance, created, *args, **kwargs):
    if created:
        # TODO: Send Inventory Request Email to an Admin
        pass
