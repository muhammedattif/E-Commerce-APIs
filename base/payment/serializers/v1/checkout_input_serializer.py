# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.users.models import Address
from base.utility.utility_serializers import ErrorHandledSerializerMixin


class CheckoutInputSerializer(ErrorHandledSerializerMixin, serializers.Serializer):
    address_id = serializers.IntegerField(required=True)

    def validate_address_id(self, address_id):
        request = self.context.get("request")
        address = Address.objects.filter(id=address_id, user=request.user).last()
        if not address:
            raise serializers.ValidationError("Invalid Address.")
        self.address = address
        return address_id
