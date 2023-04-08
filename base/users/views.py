# Python Standard Library Imports
import random

# Django Imports
from django.contrib.auth.models import User

# REST Framework Imports
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .models import Customer


# Create your views here.
class GuestSignUpView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        user = User.objects.create_user("user" + str(random.randint(0, 1000000)))
        user.username = user.pk
        user.save()
        Customer.objects.create(user=user, registered=False)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
