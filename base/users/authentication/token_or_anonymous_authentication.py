# Django Imports
from django.contrib.auth.models import AnonymousUser

# REST Framework Imports
from rest_framework.exceptions import AuthenticationFailed

from .custom_token_authentication import CustomTokenAuthentication


class TokenOrAnonymousAuthentication(CustomTokenAuthentication):
    """TokenOrAnonymousAuthentication class"""

    def authenticate(self, request):
        user, token = AnonymousUser(), None
        try:
            user, token = super().authenticate(request)
        except AuthenticationFailed:
            pass
        finally:
            return user, token
