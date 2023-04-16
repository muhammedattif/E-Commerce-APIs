# Django Imports
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Other Third Party Imports
from simple_history.models import HistoricalRecords

# First Party Imports
from base.utility.choices import ApprovalActionChoices, ApprovalRequestChoices
from base.utility.functions import model_to_dict
from base.utility.functions.simple_history import adjusted_get_user


class AbstractModel(models.Model):
    """abstract model that is an entry point for common changes across all models"""

    is_active = models.BooleanField(default=True, verbose_name=_("Is Active?"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True


class AbstractModelWithHistory(AbstractModel):
    """abstract model with history"""

    history = HistoricalRecords(get_user=adjusted_get_user, verbose_name=_("History"), inherit=True)

    class Meta:
        abstract = True


class AbstractModelWithApproval(AbstractModel):
    """abstract model with Approval"""

    PRIMARY_CLASS = None
    APPROVAL_FIELDS = []
    NON_EDITABLE_FIELDS = []

    updated_fields = models.JSONField(
        null=True,
        blank=True,
        default=dict,
    )
    primary_instance_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Primary Instance"),
    )
    primary_instance_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    primary_instance = GenericForeignKey(
        "primary_instance_type",
        "primary_instance_id",
    )

    request_type = models.IntegerField(
        choices=ApprovalRequestChoices.choices,
        verbose_name=_("Request Type"),
    )
    action = models.IntegerField(
        default=ApprovalActionChoices.SUBMITTED,
        choices=ApprovalActionChoices.choices,
        verbose_name=_("Action"),
    )
    action_taken_by = models.ForeignKey(
        "base.User",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Action Taken By"),
    )
    action_taken_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Action Taken At"),
    )

    class Meta:
        abstract = True

    def __str__(self):
        if self.primary_instance:
            return self.primary_instance.__str__()
        return "{0} No #{1}".format(
            self.__class__._meta.verbose_name,
            self.id,
        )

    def send_declined_email(self):
        pass

    def send_approval_email(self):
        pass

    @classmethod
    def get_many_to_many_fields(cls):
        opts = cls.PRIMARY_CLASS._meta
        return [f.name for f in opts.get_fields() if f.many_to_many]

    @classmethod
    def exclude_many_to_many_fields(cls, fields_dict):
        many_to_many_fields = cls.get_many_to_many_fields()
        return {key: value for key, value in fields_dict.items() if key not in many_to_many_fields}

    @classmethod
    def create_addition_request(cls, **kwargs):
        many_to_many_fields = cls.get_many_to_many_fields()

        approval_instance = cls.objects.create(
            request_type=ApprovalRequestChoices.ADDITION, **cls.exclude_many_to_many_fields(kwargs)
        )
        for field in many_to_many_fields:
            values = kwargs.get(field, None)
            if values:
                getattr(approval_instance, field).set(values)

        return approval_instance

    @classmethod
    def create_updation_request(cls, primary_instance, **kwargs):
        many_to_many_fields = cls.get_many_to_many_fields()
        filtered_kwargs = {key: value for key, value in kwargs.items() if key not in cls.NON_EDITABLE_FIELDS}
        primary_instance_dict = model_to_dict(
            primary_instance,
            fields=[field.name for field in cls.PRIMARY_CLASS._meta.fields],
            exclude=["id"],
        )
        # Override fields with the new updated values
        for key, value in filtered_kwargs.items():
            primary_instance_dict[key] = value
            if key in many_to_many_fields:
                filtered_kwargs[key] = list(filtered_kwargs[key].values("id"))

        approval_instance = cls.objects.create(
            primary_instance=primary_instance,
            request_type=ApprovalRequestChoices.UPDATION,
            updated_fields=filtered_kwargs,
            **cls.exclude_many_to_many_fields(primary_instance_dict)
        )
        for field in many_to_many_fields:
            values = kwargs.get(field, None)
            if values:
                getattr(approval_instance, field).set(list(values))
        return approval_instance

    @classmethod
    def create_deletion_request(cls, primary_instance):
        many_to_many_fields = cls.get_many_to_many_fields()
        approval_instance = cls.objects.create(
            primary_instance=primary_instance,
            request_type=ApprovalRequestChoices.DELETION,
            **model_to_dict(
                primary_instance,
                fields=[field.name for field in cls.PRIMARY_CLASS._meta.fields],
                exclude=["id"],
            )
        )
        for field in many_to_many_fields:
            values = getattr(primary_instance, field, None).all()
            if values:
                getattr(approval_instance, field).set(values)
                approval_instance.save()

        return approval_instance

    def _create_primary_instance(self):
        many_to_many_fields = self.__class__.get_many_to_many_fields()
        primary_instance = self.PRIMARY_CLASS.objects.create(
            **model_to_dict(
                self,
                fields=[field.name for field in self.PRIMARY_CLASS._meta.fields],
                exclude=["id"],
            )
        )
        for field in many_to_many_fields:
            values = getattr(self, field, None).all()
            if values:
                getattr(primary_instance, field).set(values)
                primary_instance.save()

        return True

    def _update_primary_instance(self):
        for field in self.APPROVAL_FIELDS:
            self.__setattr__(field, getattr(self.primary_instance, field))
        return True

    def _soft_delete_primary_instance(self):
        self.primary_instance.is_active = False
        self.primary_instance.save()
        return True

    def approve(self, action_user):
        if self.action != ApprovalActionChoices.SUBMITTED:
            return False

        if self.request_type == ApprovalRequestChoices.ADDITION:
            is_created = self._create_primary_instance()
            if not is_created:
                return False

        elif self.request_type == ApprovalRequestChoices.UPDATION:
            is_updated = self._update_primary_instance()
            if not is_updated:
                return False

        elif self.request_type == ApprovalRequestChoices.DELETION:
            is_deleted = self._soft_delete_primary_instance()
            if not is_deleted:
                return False

        self.action = ApprovalActionChoices.APPROVED
        self.action_taken_at = timezone.now()
        self.action_taken_by = action_user
        self.save()
        self.send_approval_email()
        return True

    def decline(self, action_user):
        if self.action != ApprovalActionChoices.SUBMITTED:
            return False

        self.action = ApprovalActionChoices.DECLINED
        self.action_taken_at = timezone.now()
        self.action_taken_by = action_user
        self.save()
        self.send_declined_email()
        return True
