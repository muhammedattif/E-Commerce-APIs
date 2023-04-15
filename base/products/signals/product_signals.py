# Django Imports
from django.db.models.signals import pre_save
from django.dispatch import receiver

# First Party Imports
from base.products.models import Product


@receiver(pre_save, sender=Product)
def product_pre_save_signal(sender, instance, *args, **kwargs):
    pass
