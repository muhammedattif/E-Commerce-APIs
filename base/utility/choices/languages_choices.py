# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class Languages(models.TextChoices):
    EN = "EN", _("English")
    AR = "AR", _("Arabic")
