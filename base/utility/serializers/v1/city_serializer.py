# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.utility.choices import Languages
from base.utility.models import City


class CitySerializer(serializers.ModelSerializer):
    """City serializer"""

    name = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ("id", "name")

    def get_name(self, city):
        lang = self.context.get("lang", Languages.AR)
        if lang == Languages.EN:
            return city.en_name
        return city.ar_name
