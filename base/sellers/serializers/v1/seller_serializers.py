# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.users.models import User


class SellerBasicinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
        ]
