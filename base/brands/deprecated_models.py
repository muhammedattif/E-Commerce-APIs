# Django Imports
from django.db import models

# Other Third Party Imports
from apps.users.models import Customer

# Create your models here.


class Brand(models.Model):
    def brand_media_directory_path(instance, filename):
        return "brands/{0}/{1}".format(instance.name, filename)

    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to=brand_media_directory_path)

    @property
    def items(self):
        return InventoryItemColor.objects.filter(inventory_item__collection__brand=self)

    def is_user_fav(self, user):
        return CustomerFavoriteBrand.objects.filter(brand=self, customer__user=user).exists()

    def __str__(self) -> str:
        return self.name


class Collection(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.brand) + " " + self.name

    class Meta:
        unique_together = ("brand", "name")


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class ClothingType(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    show_in_search_list = models.BooleanField(default=True)
    search_list_priority = models.IntegerField()

    class Meta:
        verbose_name = "Clothing Type"
        unique_together = (("name", "category"), ("category", "search_list_priority"))

    def __str__(self) -> str:
        return str(self.category) + " " + self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=50)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    clothing_types = models.ManyToManyField(ClothingType, blank=True)

    # TODO: change clothing types to manytomany and do validate field method by validator
    # to ensure only 4 types are entered and see if the validator is checked by the serializer

    class Meta:
        verbose_name = "Inventory Item"

    def __str__(self) -> str:
        return str(self.collection) + " " + self.name + " " + str(self.id)


class InventoryItemColor(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    @property
    def image(self):
        return InventoryItemColorImage.objects.filter(inventory_item_color=self).order_by("order").first().image

    class Meta:
        verbose_name = "Inventory Item Color"
        unique_together = ("inventory_item", "color")

    def __str__(self) -> str:
        return self.color + " " + str(self.inventory_item)


class InventoryItemColorSize(models.Model):
    size_choices = [
        ("xxxsmall", "3XS"),
        ("xxsmall", "2XS"),
        ("xsmall", "XS"),
        ("small", "S"),
        ("medium", "M"),
        ("large", "L"),
        ("xlarge", "XL"),
        ("xxlarge", "2XL"),
        ("xxxlarge", "3XL"),
    ]
    inventory_item_color = models.ForeignKey(InventoryItemColor, on_delete=models.CASCADE)
    size = models.CharField(max_length=50, choices=size_choices)
    stock = models.IntegerField()

    class Meta:
        verbose_name = "Inventory Item Color Size"
        unique_together = ("inventory_item_color", "size")

    def __str__(self) -> str:
        return str(self.inventory_item_color) + " " + self.get_size_display()


class InventoryItemColorImage(models.Model):
    def item_media_directory_path(instance, filename):
        inventory_item = instance.inventory_item_color.inventory_item
        brand = inventory_item.collection.brand.name
        collection = inventory_item.collection.name
        inventory_item_name = inventory_item.name
        color = instance.inventory_item_color.color
        return "brands/{0}/{1}/{2}/{3}/{4}".format(brand, collection, inventory_item_name, color, filename)

    inventory_item_color = models.ForeignKey(InventoryItemColor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=item_media_directory_path)
    order = models.IntegerField()

    class Meta:
        verbose_name = "Inventory Item Color Image"
        unique_together = ("inventory_item_color", "order")

    def __str__(self) -> str:
        return str(self.inventory_item_color) + " Image No. " + str(self.order)


class CustomerFavoriteBrand(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Customer Favorite Brand"
        unique_together = ("customer", "brand")

    def __str__(self) -> str:
        return str(self.customer) + " " + str(self.brand)


class CustomerFavoriteItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItemColor, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Customer Favorite Item"
        unique_together = ("customer", "item")

    def __str__(self) -> str:
        return str(self.customer) + " " + str(self.item)


class CustomerBagItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItemColorSize, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Customer Bag Item"
        unique_together = ("customer", "item")

    def __str__(self) -> str:
        return str(self.customer) + " " + str(self.item)


class HomePageSection(models.Model):
    section_type_choices = [
        ("item_image", "Item Image"),
        ("brand_image", "Brand Image"),
        ("items", "Items"),
        ("brands", "Brands"),
    ]

    order = models.IntegerField(unique=True)
    show_on_home_page = models.BooleanField(default=True)
    title = models.CharField(max_length=50, blank=True)
    text = models.TextField(blank=True)
    section_type = models.CharField(max_length=50, choices=section_type_choices)
    item = models.ForeignKey(InventoryItemColor, on_delete=models.CASCADE, null=True, blank=True, related_name="item")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name="brand")
    items = models.ManyToManyField(InventoryItemColor, blank=True, related_name="items")
    brands = models.ManyToManyField(Brand, blank=True, related_name="brands")

    class Meta:
        verbose_name = "Home Page Section"

    # TODO: Clean method to ensure right section data is entered for each section
    def clean(self) -> None:
        return super().clean()

    def __str__(self) -> str:
        return "Home Page Section No. " + str(self.order)
