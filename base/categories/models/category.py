# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Other Third Party Imports
from mptt.models import MPTTModel, TreeForeignKey

# First Party Imports
from base.utility.functions import get_media_upload_directory_path


class Category(MPTTModel):
    """MPTT Category model"""

    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="childs",
        on_delete=models.SET_NULL,
        verbose_name=_("Parent"),
    )
    image = models.ImageField(blank=True, null=True, upload_to=get_media_upload_directory_path, verbose_name=_("Image"))
    show_in_search_list = models.BooleanField(default=True, verbose_name=_("Show in Search List"))
    search_list_priority = models.IntegerField(null=True, blank=True, verbose_name=_("Search List Periority"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        db_table = "categories_category"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        unique_together = ("name", "parent")

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return " -> ".join(full_path[::-1])
