# Django Imports
from django.contrib import admin

# First Party Imports
from base.payment.admin_forms import CartItemForm
from base.payment.models import CartItem
from base.utility.utility_admin import AbstractModelAdmin


@admin.register(CartItem)
class CartItemAdmin(AbstractModelAdmin):
    form = CartItemForm
    list_filter = ("product__name", "cart", "model", "quantity")
    list_display = ("product", "cart", "model", "quantity")
    autocomplete_fields = ["product"]
    readonly_fields = ("quantity",)
    list_select_related = ["product", "model"]
