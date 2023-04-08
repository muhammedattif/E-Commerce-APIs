# Django Imports
from django.contrib import admin

from .deprecated_models import (
    Brand,
    Category,
    ClothingType,
    Collection,
    CustomerBagItem,
    CustomerFavoriteBrand,
    CustomerFavoriteItem,
    HomePageSection,
    InventoryItem,
    InventoryItemColor,
    InventoryItemColorImage,
    InventoryItemColorSize,
)

# Register your models here.

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ClothingType)
admin.site.register(Collection)
admin.site.register(CustomerBagItem)
admin.site.register(CustomerFavoriteBrand)
admin.site.register(CustomerFavoriteItem)
admin.site.register(HomePageSection)


class InventoryItemColorImageInLine(admin.TabularInline):
    model = InventoryItemColorImage
    extra = 1


class InventoryItemColorSizeInLine(admin.TabularInline):
    model = InventoryItemColorSize
    extra = 1


class InventoryItemColorAdmin(admin.ModelAdmin):
    inlines = (InventoryItemColorSizeInLine, InventoryItemColorImageInLine)
    extra = 1


admin.site.register(InventoryItemColor, InventoryItemColorAdmin)


class InventoryItemColorInLine(admin.TabularInline):
    model = InventoryItemColor
    extra = 1
    show_change_link = True


class InventoryItemAdmin(admin.ModelAdmin):
    inlines = (InventoryItemColorInLine,)


admin.site.register(InventoryItem, InventoryItemAdmin)
