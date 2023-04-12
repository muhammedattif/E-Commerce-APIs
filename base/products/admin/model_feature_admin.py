# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.models import ModelFeature, ModelOption
from base.utility.utility_admin import AbstractModelAdmin


class OptionInline(admin.StackedInline):
    model = ModelOption
    extra = 0


@admin.register(ModelFeature)
class ModelFeatureAdmin(AbstractModelAdmin):
    list_display = ["id", "name", "model"]
    list_filter = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    list_select_related = ["model"]
    inlines = [OptionInline]
