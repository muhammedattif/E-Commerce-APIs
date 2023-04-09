# Django Imports
from django.contrib import admin

# First Party Imports
from base.users.models import Referral
from base.utility.utility_admin import AdminListPerPageMixin


@admin.register(Referral)
class ReferralAdmin(AdminListPerPageMixin, admin.ModelAdmin):
    list_display = ["referent", "is_first_item_purchased", "created_at"]
    list_filter = ["referent", "is_first_item_purchased", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
