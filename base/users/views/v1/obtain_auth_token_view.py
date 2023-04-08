# Django Imports
from django.contrib.auth import login

# REST Framework Imports
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

# First Party Imports
from base.users.serializers import ObtainAuthTokenInputSerializer
from base.utility.response_codes import GeneralCodes


class ObtainAuthTokenView(APIView):
    """Obtain Auth Token view"""

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = ObtainAuthTokenInputSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(
                {
                    "code": serializer.code,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "authentication_scheme": TokenAuthentication.keyword,
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )
