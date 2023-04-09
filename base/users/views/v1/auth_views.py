# Django Imports
from django.contrib.auth import login

# REST Framework Imports
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

# First Party Imports
from base.users.serializers import ChangePasswordInputSerializer, ObtainAuthTokenInputSerializer
from base.utility.response_codes import GeneralCodes


class AuthViewSet(viewsets.GenericViewSet):
    @action(
        methods=["POST"],
        detail=False,
        url_path="obtain-token",
        authentication_classes=[],
        permission_classes=[],
    )
    def obtain_token(self, request, *args, **kwargs):
        """Obtain Auth Token view"""

        serializer = ObtainAuthTokenInputSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(
                {
                    "codes": serializer.codes,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.user
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

    @action(methods=["POST"], detail=False, url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        """Change Password view"""

        serializer = ChangePasswordInputSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid(raise_exception=False):
            return Response(
                {
                    "code": serializer.code,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_password = serializer.validated_data.get("new_password")
        request.user.set_password(new_password)
        request.user.save()
        request.user.generate_new_token()

        return Response({"code": GeneralCodes.SUCCESS}, status=status.HTTP_200_OK)
