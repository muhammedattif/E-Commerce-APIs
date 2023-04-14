# Django Imports
from django.db.models.signals import post_save
from django.dispatch import receiver

# First Party Imports
from base.products.models import Product


@receiver(post_save, sender=Product)
def product_pre_save_signal(sender, instance, *args, **kwargs):
    old_instance = sender.objects.filter(id=instance.id).first()
    if not instance.id or (old_instance and old_instance.is_approved != instance.is_approved) and instance.is_approved:
        # TODO: Send Approval Email to the Seller
        pass
