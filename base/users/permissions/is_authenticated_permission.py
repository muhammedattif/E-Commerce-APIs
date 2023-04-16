# Django Imports
from django.utils.translation import gettext_lazy as _

# REST Framework Imports
from rest_framework.permissions import IsAuthenticated

# First Party Imports
from base.utility.response_codes import UsersCodes


class IsAuthenticatedPermission(IsAuthenticated):
    message = {
        "message": _("You do not have permission to perform this action."),
        "code": UsersCodes.NOT_AUTHENTICATED,
    }
