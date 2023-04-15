# Django Imports
from django.db.models.signals import pre_save
from django.dispatch import receiver

# First Party Imports
from base.products.models import ModelApproval, ProductApproval
from base.utility.choices import ApprovalActionChoices


@receiver(pre_save, sender=ProductApproval)
@receiver(pre_save, sender=ModelApproval)
def approval_pre_save_signal(sender, instance, *args, **kwargs):
    if instance.id:
        old_instance = sender.objects.filter(id=instance.id).first()
        if old_instance.status != instance.status:
            if instance.status == ApprovalActionChoices.APPROVED:
                instance.send_approval_email()
        elif instance.status == ApprovalActionChoices.DECLINED:
            instance.send_declined_email()
