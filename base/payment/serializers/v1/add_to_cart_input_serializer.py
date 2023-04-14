# Django Imports
from django.core.validators import MinValueValidator

# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.products.models import Model, Product
from base.utility.utility_serializers import ErrorHandledSerializerMixin


class AddToCartInputerializer(ErrorHandledSerializerMixin, serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True, is_approved=True))
    model = serializers.PrimaryKeyRelatedField(queryset=Model.objects.filter(is_active=True))
    quantity = serializers.IntegerField(
        default=1,
        required=False,
        validators=[MinValueValidator(1)],
    )

    def validate(self, data):
        product = data.get("product")
        model = data.get("model")
        if model.product != product:
            raise serializers.ValidationError({"model": "Invalid Model"})
        return data
