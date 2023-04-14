# Django Imports
from django.dispatch import receiver

# Other Third Party Imports
from simple_history.signals import pre_create_historical_record

# First Party Imports
from base.products.models import Model


@receiver(pre_create_historical_record)
def pre_create_historical_record_callback(sender, **kwargs):
    instance = kwargs["instance"]
    history_instance = kwargs["history_instance"]
    if isinstance(instance, Model):
        instance.refresh_from_db()
        history_instance.inventory_quantity = instance.inventory_quantity
