# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractTracker(models.Model):
    user = models.ForeignKey("base.User", null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("User"))
    clicks = models.PositiveIntegerField(default=0, verbose_name=_("Clicks"))

    class Meta:
        abstract = True

    @classmethod
    def add(cls, user, **kwargs):
        if user.is_anonymous:
            user = None

        tracker, created = cls.objects.get_or_create(user=user, **kwargs)
        tracker.clicks = models.F("clicks") + 1
        tracker.save()
        return True
