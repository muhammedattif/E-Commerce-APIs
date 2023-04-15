# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class ApprovalActionChoices(models.IntegerChoices):
    SUBMITTED = 0, _("Submitted")
    DECLINED = 1, _("Declined")
    APPROVED = 2, _("Approved")
