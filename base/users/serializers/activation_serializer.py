# Django Imports
from django.contrib.auth.tokens import default_token_generator

# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.users.models import User
from base.utility.response_codes import UsersCodes
from base.utility.utility_serializers import ErrorHandledSerializerMixin


class ActivationSerializer(ErrorHandledSerializerMixin, serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # uid validation have to be here, because validate_<field_name>
        # doesn't work with modelserializer
        try:
            uid = User.decode_uid(self.initial_data.get("uid", ""))
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            self.code = UsersCodes.INVALID_UID
            raise serializers.ValidationError("Invalid UID")

        is_token_valid = default_token_generator.check_token(
            self.user,
            self.initial_data.get("token", ""),
        )
        if not is_token_valid:
            self.code = UsersCodes.INVALID_TOKEN
            raise serializers.ValidationError({"Invalid Token"})

        if self.user.is_active:
            self.code = UsersCodes.ALREADY_ACTIVATED
            raise serializers.ValidationError({"User is already active"})

        return validated_data
