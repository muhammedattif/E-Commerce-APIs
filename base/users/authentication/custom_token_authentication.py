# Django Imports
from django.utils.translation import gettext_lazy as _

# REST Framework Imports
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    """CustomTokenAuthentication class"""

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)

        if user.is_suspended:
            msg = _("User has been temporarily blocked due to violating the rules.")
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_email_verified:
            msg = _("User's email is not verified.")
            raise exceptions.AuthenticationFailed(msg)

        return user, token
