# REST Framework Imports
from rest_framework import permissions

# First Party Imports
from base.utility.response_codes import UsersCodes


class BuyerPermission(permissions.BasePermission):
    message = {
        "message": "Permission Denied",
        "code": UsersCodes.INVALID_ACCOUNT_TYPE,
    }

    def has_permission(self, request, view):
        if not request.user.is_buyer:
            return False
        return True
