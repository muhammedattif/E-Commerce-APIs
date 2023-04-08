# REST Framework Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# First Party Imports
from base.users.serializers import ActivationSerializer
from base.utility.response_codes import GeneralCodes


class UserActivationView(APIView):
    """UserActivation View"""

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        context = {
            "request": request,
            "format": self.format_kwarg,
            "view": self,
        }
        serializer = ActivationSerializer(data=request.data, context=context)
        if not serializer.is_valid(raise_exception=False):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.user
        user.is_active = True
        user.save()

        # Send confirmation email
        user.send_confirmation_email()

        return Response(
            {
                "code": GeneralCodes.SUCCESS,
            },
            status=status.HTTP_200_OK,
        )
