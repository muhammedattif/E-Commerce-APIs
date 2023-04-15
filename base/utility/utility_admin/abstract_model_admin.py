# Django Imports
from django.contrib import admin, messages

# Other Third Party Imports
from simple_history.admin import SimpleHistoryAdmin

# First Party Imports
from base.utility.utility_admin.forms import AbstractApprovalForm


class AbstractModelAdmin(SimpleHistoryAdmin):
    """abstract model admin that is the entry point for common changes across all Model admins"""

    list_per_page = 10
    non_selection_actions = []

    def get_non_selection_actions(self, request):
        """returns a list of actions that do not need a selection from queryset"""
        return self.non_selection_actions

    def changelist_view(self, request, extra_context=None):
        if "action" in request.POST and request.POST["action"] in self.get_non_selection_actions(request):
            if not request.POST.getlist("_selected_action"):
                post = request.POST.copy()
                post.update({"_selected_action": None})
                request._set_post(post)
        return super().changelist_view(request, extra_context)


class AbstractModelAdminWithApprovalMixin:
    """Abstract Model admin With Approval Actions"""

    form = AbstractApprovalForm
    actions = ["decline", "approve"]

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return [
            "id",
            "primary_instance",
            "request_type",
            "action",
            "action_taken_by",
            "action_taken_at",
        ] + list(list_display)

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        return [
            "primary_instance_id",
            "request_type",
            "action",
            "action_taken_by",
            "action_taken_at",
        ] + list(list_filter)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return [
            "request_type",
            "primary_instance",
            "action",
            "action_taken_by",
            "action_taken_at",
        ] + list(fields)

    def get_readonly_fields(self, request, obj=None):
        read_only_fields = super().get_readonly_fields(request, obj)
        return [
            "request_type",
            "action",
            "primary_instance",
            "action_taken_by",
            "action_taken_at",
            "created_at",
        ] + list(read_only_fields)

    def decline(self, request, queryset):
        for instance in queryset:
            is_declined = instance.decline(action_user=request.user)
            if is_declined:
                message = "Change Request {0} has been Declined".format(instance.id)
                self.message_user(request, message, level=messages.SUCCESS)
            else:
                message = "Change Request {0} cannot be Declined".format(instance.id)
                self.message_user(request, message, level=messages.ERROR)
        return

    def approve(self, request, queryset):
        for instance in queryset:
            is_approved = instance.approve(action_user=request.user)
            if is_approved:
                message = "Change Request {0} has been Approved".format(instance.id)
                self.message_user(request, message, level=messages.SUCCESS)
            else:
                message = "Change Request {0} cannot be Approved".format(instance.id)
                self.message_user(request, message, level=messages.ERROR)
        return

    def has_add_permission(self, request) -> bool:
        return False


class AbstractModelAdminWithApprovalInlineMixin:
    """Abstract Model Inline With Approval Actions"""

    form = AbstractApprovalForm

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return [
            "request_type",
            "primary_instance",
            "action",
            "action_taken_by",
            "action_taken_at",
        ] + list(fields)

    def get_readonly_fields(self, request, obj=None):
        read_only_fields = super().get_readonly_fields(request, obj)
        return [
            "request_type",
            "action",
            "primary_instance",
            "action_taken_by",
            "action_taken_at",
            "created_at",
        ] + list(read_only_fields)


class AbstractStackedInline(admin.StackedInline):
    """abstract model admin that is the entry point for common changes across all StackedInline admins"""


class AbstractTabularInline(admin.TabularInline):
    """abstract model admin that is the entry point for common changes across all TabularInline admins"""
