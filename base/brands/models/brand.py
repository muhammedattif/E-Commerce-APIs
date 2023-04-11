# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.brands.managers import BrandManager
from base.utility.media_upload_directories import get_media_upload_directory_path
from base.utility.utility_models import AbstractModel


class Brand(AbstractModel):
    """
    Brand Model
    """

    seller = models.ForeignKey("base.User", on_delete=models.CASCADE, verbose_name=_("Seller"))
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to=get_media_upload_directory_path)

    objects = BrandManager()

    class Meta:
        db_table = "brands_brand"
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self) -> str:
        return self.name
