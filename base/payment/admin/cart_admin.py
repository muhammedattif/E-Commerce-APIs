# Django Imports
from django.contrib import admin

# First Party Imports
from base.payment.admin_forms import CartItemForm
from base.payment.models import Cart, CartItem
from base.utility.utility_admin import AbstractModelAdmin, AbstractStackedInline


class CartItemInline(AbstractStackedInline):
    model = CartItem
    form = CartItemForm
    autocomplete_fields = ["product"]
    extra = 0


@admin.register(Cart)
class CartAdmin(AbstractModelAdmin):
    list_filter = ["user", "sub_total", "total", "discount", "taxes"]
    list_display = ["user", "sub_total", "total", "discount", "taxes"]
    readonly_fields = ["sub_total", "total", "discount", "taxes"]
    inlines = [CartItemInline]
