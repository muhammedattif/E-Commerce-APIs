# REST Framework Imports
from rest_framework import permissions


class BuyerPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        permitted = super().has_permission(request=request, view=view)
        if not permitted:
            return False

        if not request.user.is_buyer:
            return False

        return True
