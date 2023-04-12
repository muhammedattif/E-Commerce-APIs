# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.utility.choices import Languages
from base.utility.models import Governorate


class GovernorateSerializer(serializers.ModelSerializer):
    """Governorate serializer"""

    name = serializers.SerializerMethodField()

    class Meta:
        model = Governorate
        fields = ("id", "name")

    def get_name(self, governorate):
        lang = self.context.get("lang", Languages.AR)
        if lang == Languages.EN:
            return governorate.en_name
        return governorate.ar_name
