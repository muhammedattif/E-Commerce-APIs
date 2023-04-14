# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel


class Favorite(AbstractModel):
    """
    Favorite model
    """

    user = models.OneToOneField(
        "base.User",
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("User"),
    )
    brands = models.ManyToManyField("base.Brand", blank=True, verbose_name=_("Brands"))
    products = models.ManyToManyField("base.Product", blank=True, verbose_name=_("Products"))

    class Meta:
        db_table = "users_favorites"
        verbose_name = _("Favorite")
        verbose_name_plural = _("Favorites")

    def __str__(self):
        return "{0}".format(self.user.email)
