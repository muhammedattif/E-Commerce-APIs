# REST Framework Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# First Party Imports
from base.users.serializers import ChangePasswordInputSerializer
from base.utility.response_codes import GeneralCodes


class ChangePasswordView(APIView):
    """Change Password View"""

    def put(self, request, user_id):

        serializer = ChangePasswordInputSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid(raise_exception=False):
            return Response(
                {
                    "code": serializer.code,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response({"code": GeneralCodes.SUCCESS}, status=status.HTTP_200_OK)
