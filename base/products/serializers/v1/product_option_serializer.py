# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.products.models import ProductOption


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = [
            "id",
            "name",
        ]
