# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.payment.models import OrderTracker
from base.payment.utils.choices import OrderTrackingStatusChoices


class OrderTrackerSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = OrderTracker
        fields = [
            "id",
            "status",
            "estimated_date",
            "additional_info",
            "created_at",
            "updated_at",
        ]

    def get_status(self, obj):
        return OrderTrackingStatusChoices(obj.status).label
