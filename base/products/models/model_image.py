# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.utility import AbstractModel
from base.utility.functions import get_media_upload_directory_path


class ModelImage(AbstractModel):

    model = models.ForeignKey(
        "base.Model",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Model"),
    )
    image = models.ImageField(
        upload_to=get_media_upload_directory_path,
        verbose_name=_("Image"),
        help_text=_("Images only"),
    )

    class Meta:
        db_table = "products_model_images"
        verbose_name = _("Model Image")
        verbose_name_plural = _("Model Images")

    def __str__(self) -> str:
        return self.model.__str__()
