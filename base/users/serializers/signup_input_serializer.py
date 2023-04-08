# Django Imports
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.users.models import User
from base.utility.response_codes import UsersCodes
from base.utility.utility_serializers import ErrorHandledSerializerMixin


class SignUpInputSerializer(ErrorHandledSerializerMixin, serializers.ModelSerializer):
    """SignUp Input Serializer"""

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            self.code = UsersCodes.PASSWORD_NOT_MATCH
            raise serializers.ValidationError({"password": "Password does not match."})

        del data["password2"]
        return data

    def validate_password(self, password):
        """validate password field"""
        try:
            # validate the password and catch the exception
            validate_password(password)
            # the exception raised here is different than serializers.ValidationError
        except ValidationError as e:
            self.code = UsersCodes.INVALID_PASSWORD_CRITERIA
            raise serializers.ValidationError(list(e.messages))

        return password

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)
