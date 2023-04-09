# Django Imports
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.utility.response_codes import UsersCodes
from base.utility.utility_serializers import ErrorHandledSerializerMixin


class ChangePasswordInputSerializer(ErrorHandledSerializerMixin, serializers.Serializer):
    """
    Input Serializer for password change endpoint.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Validate attrs
        """
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")

        request = self.context.get("request")
        user = request.user
        if not user.check_password(old_password):
            self.code = UsersCodes.INVALID_OLD_PASSWORD
            raise serializers.ValidationError(
                {
                    "old_password": "Old password is wrong.",
                },
            )

        try:
            # validate the password and catch the exception
            validate_password(new_password)
            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            self.code = UsersCodes.INVALID_PASSWORD_CRITERIA
            raise serializers.ValidationError(
                {
                    "new_password": list(e.messages),
                },
            )

        return attrs
