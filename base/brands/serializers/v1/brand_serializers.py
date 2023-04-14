# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.brands.models import Brand
from base.sellers.serializers import SellerBasicInfoSerializer


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "image",
        ]


class BrandDetailSerializer(serializers.ModelSerializer):
    seller = SellerBasicInfoSerializer(many=False, read_only=True)

    class Meta:
        model = Brand
        fields = [
            "id",
            "seller",
            "name",
            "image",
        ]
