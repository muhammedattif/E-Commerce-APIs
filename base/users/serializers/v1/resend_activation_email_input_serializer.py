# Django Imports

# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.users.models import User
from base.utility.utility_serializers import ErrorHandledSerializerMixin


class ResendActivationInputSerializer(ErrorHandledSerializerMixin, serializers.Serializer):
    """ResendActivationInput Serializer"""

    email = serializers.EmailField()

    def validate_email(self, email):
        """validates email field"""
        user = User.objects.filter(email=email, is_active=False).last()
        if not user:
            raise serializers.ValidationError("Invalid email")
        self.user = user
        return email
