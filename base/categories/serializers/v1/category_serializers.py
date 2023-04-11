# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.categories.models import Category


class AbstractCategorySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image"]


class CategorySerializer(AbstractCategorySerialiser):
    "Category Serializer"


class CategoryDetailSerializer(CategorySerializer):
    childs = CategorySerializer(many=True, read_only=True)

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + [
            "childs",
        ]
