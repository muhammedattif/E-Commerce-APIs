# First Party Imports
from base.utility.constants import DEVELOPER_GROUP

from .is_authenticated_permission import IsAuthenticatedPermission


class DeveloperPermission(IsAuthenticatedPermission):
    def has_permission(self, request, view):
        permitted = super().has_permission(request=request, view=view)
        if not permitted:
            return False

        if not request.user.groups.filter(name=DEVELOPER_GROUP).exists():
            return False

        return True
