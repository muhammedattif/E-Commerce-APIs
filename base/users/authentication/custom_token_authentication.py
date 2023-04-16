# Django Imports
from django.utils.translation import gettext_lazy as _

# REST Framework Imports
from rest_framework import exceptions
from rest_framework.authtoken.models import Token

# First Party Imports
from base.utility.response_codes import UsersCodes

from .abstract_auth import AbstractAuth


class CustomTokenAuthentication(AbstractAuth):
    """CustomTokenAuthentication class"""

    def authenticate_credentials(self, key):
        token = Token.objects.select_related("user").filter(key=key).first()
        if not token:
            msg = _("Invalid token.")
            raise exceptions.AuthenticationFailed(
                detail={
                    "message": msg,
                    "code": UsersCodes.INVALID_AUTH,
                },
            )
        return (token.user, token)
