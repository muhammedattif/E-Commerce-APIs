# Django Imports
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# First Party Imports
from base.payment.models import Order
from base.payment.utils.choices import OrderStatusChoices


@receiver(post_save, sender=Order)
def order_post_save_signal(sender, instance, created, *args, **kwargs):
    if created:
        # Update order items status
        instance.update_order_items_status()
        # Copy address data
        instance.first_name = instance.address.first_name
        instance.last_name = instance.address.last_name
        instance.email = instance.address.email
        instance.governorate = instance.address.governorate
        instance.city = instance.address.city
        instance.street_1 = instance.address.street_1
        instance.street_2 = instance.address.street_2
        instance.landmark = instance.address.landmark
        instance.phone_number = instance.address.phone_number
        instance.country = instance.address.country

        instance.save()


@receiver(pre_save, sender=Order)
def order_pre_save_signal(sender, instance, *args, **kwargs):
    if instance.id:
        old_instance = Order.objects.get(id=instance.id)
        if old_instance.status != instance.status:

            if (
                old_instance.status in OrderStatusChoices.success_status_set()
                and instance.status in OrderStatusChoices.fail_status_set()
            ):
                # NOTE: Critical
                instance.rollback_order_items_inventory()

            instance.update_order_items_status()
            instance.dispatch_order_tracking()
