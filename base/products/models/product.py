# Django Imports
from django.db import models
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _

# First Party Imports
from base.products.managers import ProductManager
from base.utility import AbstractModel, AbstractModelWithApproval, AbstractModelWithHistory
from base.utility.functions import get_media_upload_directory_path


class AbstractProduct(AbstractModel):
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
        related_name="%(class)ss",
        verbose_name=_("Seller"),
    )
    is_sale = models.BooleanField(
        default=False,
        verbose_name=_("Is Sale?"),
    )
    is_our_pick = models.BooleanField(
        default=False,
        verbose_name=_("Is our Pick?"),
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_("Is Approved?"),
    )

    class Meta:
        abstract = True


class Product(AbstractProduct, AbstractModelWithHistory):

    objects = ProductManager()

    class Meta:
        db_table = "products_products"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return "{0}| {1}".format(self.id, self.name)

    @property
    def image(self):
        # TODO: To be removed and add cover image field
        last_model = self.models.filter(images__isnull=False).last()
        if not last_model:
            return None
        last_image = last_model.images.last()
        if not last_image:
            return None
        return last_image.image

    def check_inventory(self, options=[], quantity=1):
        "Check for Product Availability in Inventory"
        # First Party Imports
        from base.products.utils.choices import InventoryStatusChoices

        options_len = len(options)
        model_queryset = self.models
        if options:
            model_queryset = model_queryset.annotate(
                total_options=Count("product_options"),
                matching_options=Count("product_options", filter=Q(product_options__in=options)),
            ).filter(
                matching_options=options_len,
                total_options=options_len,
            )
        else:
            model_queryset = model_queryset.filter(product_options=None)

        model = model_queryset.first()
        if not model:
            return model, InventoryStatusChoices.NOT_AVAILBLE

        if model.is_out_of_stock:
            return model, InventoryStatusChoices.OUT_OF_STOCK

        if not model.is_available_in_inventory(quantity=quantity):
            return model, InventoryStatusChoices.QUANTITY_UNAVAILBLE

        return model, InventoryStatusChoices.AVAILABLE


class ProductApproval(AbstractProduct, AbstractModelWithApproval):
    PRIMARY_CLASS = Product
    APPROVAL_FIELDS = [
        "name",
        "description",
        "about",
        "category",
        "collection_name",
        "material",
        "type",
        "size_guide",
    ]
    NON_EDITABLE_FIELDS = [
        "id",
        "seller_id",
        "created_at",
        "updated_at",
    ]

    class Meta:
        db_table = "products_products_approvals"
        verbose_name = _("Product Approval")
        verbose_name_plural = _("Product Approvals")
