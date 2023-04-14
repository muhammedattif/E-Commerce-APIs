# Django Imports
from django.contrib import admin, messages

# First Party Imports
from base.products.admin_forms import ModelForm
from base.products.models import Model, Product
from base.utility.utility_admin import AbstractModelAdmin, AbstractStackedInline


class ModelInline(AbstractStackedInline):
    model = Model
    form = ModelForm
    extra = 0


@admin.register(Product)
class ProductAdmin(AbstractModelAdmin):
    list_display = ["id", "seller", "name", "category", "type", "is_approved", "is_active", "created_at", "updated_at"]
    list_filter = [
        "seller",
        "name",
        "category",
        "type",
        "is_active",
        "is_approved",
        "is_our_pick",
        "created_at",
        "updated_at",
    ]
    fields = [
        "name",
        "description",
        "about",
        "category",
        "collection_name",
        "material",
        "type",
        "size_guide",
        "seller",
        "is_our_pick",
        "is_approved",
        "is_active",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["category"]
    search_fields = ["name", "description", "about"]
    ordering = ["-created_at"]
    list_select_related = ["seller", "category"]
    actions = ["select_as_our_picks", "unselect_as_our_picks"]
    inlines = [ModelInline]

    def select_as_our_picks(self, request, queryset):
        queryset.update(is_our_pick=True)
        message = "{0} has been selected as our picks".format(queryset.count())
        self.message_user(request, message, level=messages.SUCCESS)
        return

    def unselect_as_our_picks(self, request, queryset):
        queryset.update(is_our_pick=False)
        message = "{0} has been unselected as our picks".format(queryset.count())
        self.message_user(request, message, level=messages.SUCCESS)
        return
