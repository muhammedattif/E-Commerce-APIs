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

    def validate_old_password(self, old_password):
        """
        Validate old password
        """

        request = self.context.get("request")
        user = request.user

        if not user.check_password(old_password):
            self.code = UsersCodes.INVALID_OLD_PASSWORD
            raise serializers.ValidationError("Old password is wrong.")

        return old_password

    def validate_new_password(self, new_password):
        """
        Validate new password
        """
        try:
            # validate the password and catch the exception
            validate_password(new_password)
            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            self.code = UsersCodes.INVALID_PASSWORD_CRITERIA
            raise serializers.ValidationError(list(e.messages))

        return new_password

    def save(self, **kwargs):
        request = self.context.get("request")
        user = request.user

        new_password = self.validated_data.get("new_password")
        user.set_password(new_password)
        user.save()

        return user
