# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.categories.serializers import CategorySerializer
from base.products.models import Product
from base.sellers.serializers.v1 import SellerBasicInfoSerializer

from .product_feature_serializer import ProductFeatureSerializer


class ProductSerializer(serializers.ModelSerializer):

    image = serializers.FileField()
    brand_name = serializers.CharField()
    price = serializers.FloatField()

    class Meta:
        model = Product
        fields = [
            "id",
            "image",
            "name",
            "brand_name",
            "price",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField()
    price = serializers.FloatField()
    seller = SellerBasicInfoSerializer(many=False, read_only=True)
    features = ProductFeatureSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "about",
            "category",
            "brand_name",
            "collection_name",
            "material",
            "type",
            "size_guide",
            "seller",
            "price",
            "features",
        ]
