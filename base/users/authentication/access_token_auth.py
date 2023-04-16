# Django Imports
from django.utils import timezone

# REST Framework Imports
from rest_framework import exceptions

# First Party Imports
from base.users.models import SecretToken
from base.utility.response_codes import UsersCodes

from .abstract_auth import AbstractAuth


class AccessTokenAuthentication(AbstractAuth):
    """
    Header based access token authentication
    """

    def authenticate_credentials(self, token):

        secret_token = (
            SecretToken.objects.select_related("user")
            .filter(
                key=token,
                token_type=SecretToken.TokenTypes.ACCESS,
                is_active=True,
            )
            .first()
        )
        if not secret_token:
            raise exceptions.AuthenticationFailed(
                detail={
                    "message": "Invalid credentials",
                    "code": UsersCodes.INVALID_AUTH,
                },
            )

        if not secret_token.lifetime and secret_token.expires_at < timezone.now():
            raise exceptions.AuthenticationFailed(
                detail={
                    "message": "Expired credentials",
                    "code": UsersCodes.INVALID_TOKEN,
                },
            )

        return (secret_token.user, secret_token)
