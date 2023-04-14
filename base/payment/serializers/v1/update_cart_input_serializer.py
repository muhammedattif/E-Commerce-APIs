# Django Imports
from django.core.validators import MinValueValidator

# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.utility.utility_serializers import ErrorHandledSerializerMixin


class UpdateCartItemInputerializer(ErrorHandledSerializerMixin, serializers.Serializer):
    quantity = serializers.IntegerField(
        default=1,
        required=False,
        validators=[MinValueValidator(1)],
    )
