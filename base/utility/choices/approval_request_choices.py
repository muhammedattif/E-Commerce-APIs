# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class ApprovalRequestChoices(models.IntegerChoices):
    ADDITION = 0, _("Addition")
    UPDATION = 1, _("Updation")
    DELETION = 2, _("Deletion")
