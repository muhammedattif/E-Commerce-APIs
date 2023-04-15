# REST Framework Imports
from rest_framework import serializers

# Other Third Party Imports
from django_countries.serializers import CountryFieldMixin

# First Party Imports
from base.payment.models import Order
from base.payment.utils.choices import OrderStatusChoices
from base.utility.choices import Languages

from .order_item_serializer import OrderItemSerializer


class OrderSerializer(CountryFieldMixin, serializers.ModelSerializer):
    discount_percentage = serializers.FloatField()
    governorate = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ("user", "address", "is_active")

    def get_governorate(self, obj):
        lang = self.context.get("lang", Languages.EN)
        if lang == Languages.EN:
            return obj.governorate.en_name
        return obj.governorate.ar_name

    def get_city(self, obj):
        lang = self.context.get("lang", Languages.EN)
        if lang == Languages.EN:
            return obj.city.en_name
        return obj.city.ar_name

    def get_status(self, obj):
        return OrderStatusChoices(obj.status).label


class OrderDetailSerializer(OrderSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
