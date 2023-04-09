# REST Framework Imports
from rest_framework import serializers

# First Party Imports
from base.users.models import User
from base.utility.utility_serializers import ErrorHandledSerializerMixin


class UserSerializer(ErrorHandledSerializerMixin, serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    gender = serializers.ChoiceField(choices=User.GenderTypes.choices, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "gender",
            "is_seller",
            "is_buyer",
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["gender"] = User.GenderTypes(instance.gender).label
        return ret
