# Django Imports
from django.contrib.auth import authenticate

# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.users.models import User
from base.utility.response_codes import UsersCodes
from base.utility.utility_serializers import ErrorHandledSerializerMixin


class ObtainAuthTokenInputSerializer(ErrorHandledSerializerMixin, serializers.Serializer):
    """ObtainAuthTokenInput Serializer"""

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = User.objects.filter(email=email).first()
        if not user:
            self.code = UsersCodes.INVALID_CREDENTIALS
            raise serializers.ValidationError("Invalid Credentials")

        if not user.is_active:
            self.code = UsersCodes.INACTIVE_USER
            raise serializers.ValidationError("Inactive user")

        if user.is_suspended:
            self.code = UsersCodes.SUSPENDED_USER
            raise serializers.ValidationError("Suspended User")

        authenticated = authenticate(username=email, password=password)
        if not authenticated:
            self.code = UsersCodes.INVALID_CREDENTIALS
            raise serializers.ValidationError("Invalid Credentials")

        self.user = user
        return data
