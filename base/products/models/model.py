# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel
from base.utility.functions import get_media_upload_directory_path


class Model(AbstractModel):
    class ModelTypes(models.IntegerChoices):
        MALE = 0, _("Male")
        FEMALE = 1, _("Female")
        UNISEX = 3, _("Unisex")

    name = models.CharField(
        max_length=200,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    about = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("About"),
    )
    category = models.ForeignKey(
        "base.Category",
        on_delete=models.PROTECT,
        verbose_name=_("Category"),
    )
    collection_name = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=("Collection Name"),
    )
    material = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=("Material"),
    )
    type = models.IntegerField(
        choices=ModelTypes.choices,
        verbose_name=_("Type"),
    )
    size_guide = models.FileField(
        null=True,
        blank=True,
        upload_to=get_media_upload_directory_path,
        verbose_name=_("Size Guide"),
        help_text=_("PDF or Images"),
    )
    seller = models.ForeignKey(
        "base.User",
        on_delete=models.PROTECT,
        verbose_name=_("Seller"),
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_("Is Approved"),
    )

    class Meta:
        db_table = "products_models"
        verbose_name = _("Model")
        verbose_name_plural = _("Models")

    def __str__(self) -> str:
        return self.name
