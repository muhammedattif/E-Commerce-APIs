# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.payment.models import Cart

from .cart_item_serializer import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        exclude = ["user", "is_active"]
