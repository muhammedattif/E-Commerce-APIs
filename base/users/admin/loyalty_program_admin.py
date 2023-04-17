# Django Imports
from django.contrib import admin

# First Party Imports
from base.users.models import LoyaltyProgram, Referral
from base.utility.utility_admin import AbstractModelAdmin


class ReferralInline(admin.StackedInline):
    model = Referral
    extra = 0


@admin.register(LoyaltyProgram)
class LoyaltyProgramAdmin(AbstractModelAdmin):
    list_display = ["referrer", "claimed_points", "used_points", "created_at"]
    list_filter = ["referrer", "referrals__referent", "claimed_points", "used_points", "created_at"]
    readonly_fields = ["claimed_points", "used_points", "created_at", "updated_at"]
    ordering = ["-created_at"]
    inlines = [ReferralInline]
