# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.products.models import SysOption


class SysOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysOption
        fields = [
            "id",
            "name",
        ]
