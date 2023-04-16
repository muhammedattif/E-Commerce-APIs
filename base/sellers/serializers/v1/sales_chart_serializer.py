# REST Framework Imports
from rest_framework import serializers


class SalesChartSerializer(serializers.Serializer):

    date = serializers.SerializerMethodField()
    total_sales = serializers.FloatField()
    total_items_sold = serializers.IntegerField()

    def get_date(self, obj):
        return obj["created_at"]
