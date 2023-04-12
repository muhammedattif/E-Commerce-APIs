# Django Imports
from django.contrib import admin

# First Party Imports
from base.products.models import SysFeature, SysOption
from base.utility.utility_admin import AbstractModelAdmin


class OptionInline(admin.StackedInline):
    model = SysOption
    extra = 0


@admin.register(SysFeature)
class SysFeatureAdmin(AbstractModelAdmin):
    list_display = ["id", "name"]
    list_filter = ["name"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    inlines = [OptionInline]
