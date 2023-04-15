# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.payment.models import OrderItem
from base.payment.utils.choices import OrderItemStatusChoices
from base.products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_status(self, obj):
        return OrderItemStatusChoices(obj.status).label
