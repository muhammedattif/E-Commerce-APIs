# Django Imports
from django.contrib import admin

# First Party Imports
# Register your models here.
from base.utility.models import AppConfiguration


@admin.register(AppConfiguration)
class AppConfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "referral_points")
    fieldsets = (
        (
            "Loyalty Program",
            {
                "fields": ("referral_points",),
            },
        ),
    )

    def has_add_permission(self, request):
        # check if generally has add permission
        is_allowed = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if is_allowed and self.model.objects.exists():
            is_allowed = False
        return is_allowed
