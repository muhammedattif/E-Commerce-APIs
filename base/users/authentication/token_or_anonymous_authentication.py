# Django Imports

# Django Imports
from django.contrib.auth.models import AnonymousUser

# REST Framework Imports
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TokenOrAnonymousAuthentication(TokenAuthentication):
    """TokenOrAnonymousAuthentication class"""

    def authenticate(self, request):
        user, token = AnonymousUser(), None
        try:
            user, token = super().authenticate(request)
        except AuthenticationFailed:
            pass
        finally:
            return user, token
