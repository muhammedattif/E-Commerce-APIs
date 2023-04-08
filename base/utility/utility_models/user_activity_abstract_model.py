# Django Imports
from django.db import models

# from django_currentuser.db.models import CurrentUserField


class UserActivityAbstractModel(models.Model):
    """abstract model for user activity"""

    # created_by = CurrentUserField(verbose_name=_("Created By"), related_name="%(class)ss_created")
    # updated_by = CurrentUserField(on_update=True, verbose_name=_("Updated By"), related_name="%(class)ss_updated")

    class Meta:
        abstract = True
        # indexes = [
        #     models.Index(fields=["created_by"]),
        # ]
