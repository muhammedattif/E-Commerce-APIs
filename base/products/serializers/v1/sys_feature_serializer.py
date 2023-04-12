# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.products.models import SysFeature

from .sys_option_serializer import SysOptionSerializer


class SysFeatureSerializer(serializers.ModelSerializer):
    options = SysOptionSerializer(many=True, read_only=True)

    class Meta:
        model = SysFeature
        fields = [
            "id",
            "name",
            "options",
        ]
