# REST Framework Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# First Party Imports
from base.users.serializers import SignUpInputSerializer
from base.utility.response_codes import GeneralCodes


class SignUpView(APIView):
    """SignUp View"""

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = SignUpInputSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(
                {
                    "code": GeneralCodes.INVALID_DATA,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
            },
            status=status.HTTP_201_CREATED,
        )
