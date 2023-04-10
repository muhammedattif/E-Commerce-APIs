# Django Imports
from django.db import models
from django.db.models import IntegerField, Sum
from django.db.models.functions import Coalesce


class BrandQuerySet(models.QuerySet):
    def popular(self):
        return self.annotate(
            clicks=Coalesce(
                Sum("trackers__clicks"),
                0,
                output_field=IntegerField(),
            ),
        ).order_by("-clicks")


class BrandManager(models.Manager):
    def get_queryset(self):
        return BrandQuerySet(self.model, using=self._db)

    def popular(self):
        return self.get_queryset().popular()
