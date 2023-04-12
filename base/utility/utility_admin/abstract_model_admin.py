# Django Imports
from django.contrib import admin

# Other Third Party Imports
from simple_history.admin import SimpleHistoryAdmin


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


class AbstractStackedInline(admin.StackedInline):
    """abstract model admin that is the entry point for common changes across all StackedInline admins"""


class AbstractTabularInline(admin.TabularInline):
    """abstract model admin that is the entry point for common changes across all TabularInline admins"""
