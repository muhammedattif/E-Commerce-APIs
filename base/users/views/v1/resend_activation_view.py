# REST Framework Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# First Party Imports
from base.users.serializers import ResendActivationInputSerializer
from base.utility.response_codes import GeneralCodes, UsersCodes


class ResendActivationView(APIView):
    """Resend Activation Email view"""

    authentication_classes = []
    permission_classes = []
    # TODO: Add throttle class

    def post(self, request):

        serializer = ResendActivationInputSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=False):
            return Response({"code": GeneralCodes.INVALID_DATA}, status=status.HTTP_400_BAD_REQUEST)

        is_sent = serializer.user.send_activation_email()
        if not is_sent:
            return Response({"code": UsersCodes.CANNOT_SEND_ACTIVATION_EMAIL}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"code": GeneralCodes.SUCCESS}, status=status.HTTP_400_BAD_REQUEST)
