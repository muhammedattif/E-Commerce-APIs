# Django Imports
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# First Party Imports
from base.payment.models import OrderItem
from base.payment.utils.choices import OrderItemStatusChoices


@receiver(post_save, sender=OrderItem)
def order_item_post_save_signal(sender, instance, created, *args, **kwargs):
    if created:
        if instance.status in OrderItemStatusChoices.success_status_set():
            instance.subtract_quantity_from_inventory()


@receiver(pre_delete, sender=OrderItem)
def order_item_pre_delete_signal(sender, instance, *args, **kwargs):
    if instance.status in OrderItemStatusChoices.success_status_set():
        instance.rollback_inventory_quantity()
