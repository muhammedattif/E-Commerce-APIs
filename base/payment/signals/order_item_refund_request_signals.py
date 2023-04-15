# Django Imports
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# First Party Imports
from base.payment.models import OrderItemRefundRequest


@receiver(post_save, sender=OrderItemRefundRequest)
def order_item_refund_request_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.send_request_submitted_email_to_admin_and_vendor()


@receiver(pre_save, sender=OrderItemRefundRequest)
def order_item_refund_request_pre_save(sender, instance, *args, **kwargs):
    if instance.id:
        old_instance = OrderItemRefundRequest.objects.get(id=instance.id)
        if old_instance.status != instance.status:
            instance.send_refund_status_email_to_user()
