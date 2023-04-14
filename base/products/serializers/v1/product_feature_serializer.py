# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.products.models import ProductFeature

from .product_option_serializer import ProductOptionSerializer


class ProductFeatureSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ProductFeature
        fields = [
            "id",
            "name",
            "options",
        ]
