# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.payment.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=False, read_only=True)
    model_representation = serializers.SerializerMethodField()
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = CartItem
        exclude = [
            "is_active",
            "cart",
            "model",
        ]

    def get_model_representation(self, obj):
        return obj.model.as_text
