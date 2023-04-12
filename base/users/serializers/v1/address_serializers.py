# REST Framework Imports
from rest_framework import serializers

# Other Third Party Imports
from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

# First Party Imports
from base.users.models import Address
from base.utility.models import City, Governorate
from base.utility.utility_serializers import ErrorHandledSerializerMixin


class AddressCreateSerialiser(ErrorHandledSerializerMixin, serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    country = CountryField(required=True)
    governorate = serializers.PrimaryKeyRelatedField(queryset=Governorate.objects.filter(is_active=True), required=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.filter(is_active=True), required=True)
    street_1 = serializers.CharField(required=True)
    street_2 = serializers.CharField(required=False, allow_blank=True)
    landmark = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=True)
    is_primary = serializers.BooleanField(default=False)

    class Meta:
        fields = "__all__"


class AddressUpdateSerialiser(ErrorHandledSerializerMixin, serializers.ModelSerializer):
    user = serializers.CharField(required=False, read_only=True)

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    country = CountryField(required=False)
    governorate = serializers.PrimaryKeyRelatedField(
        queryset=Governorate.objects.filter(is_active=True),
        required=False,
    )
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.filter(is_active=True), required=False)
    street_1 = serializers.CharField(required=False)
    street_2 = serializers.CharField(required=False, allow_blank=True)
    landmark = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False)
    is_primary = serializers.BooleanField(default=False)

    class Meta:
        model = Address
        fields = "__all__"


class AddressSerialiser(ErrorHandledSerializerMixin, CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "country",
            "governorate",
            "city",
            "street_1",
            "street_2",
            "landmark",
            "phone_number",
            "is_primary",
        ]
