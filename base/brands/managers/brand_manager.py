# Django Imports
from django.db import models
from django.db.models import Count, IntegerField
from django.db.models.functions import Coalesce


class BrandQuerySet(models.QuerySet):
    def popular(self):
        return self.annotate_total_clicks().order_by("-total_clicks")

    def annotate_total_clicks(self):
        return self.annotate(
            total_clicks=Coalesce(
                Count("trackers"),
                0,
                output_field=IntegerField(),
            ),
        )


class BrandManager(models.Manager):
    def get_queryset(self):
        return BrandQuerySet(self.model, using=self._db)

    def popular(self):
        return self.get_queryset().popular()

    def annotate_total_clicks(self):
        return self.get_queryset().annotate_total_clicks()
