# REST Framework Imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# First Party Imports
from base.users.authentication import AccessTokenAuthentication
from base.users.permissions import DeveloperPermission
from base.utility.response_codes import export_response_codes


class GenericViewSet(viewsets.GenericViewSet):
    authentication_classes = [AccessTokenAuthentication]
    permission_classes = [DeveloperPermission]

    @action(
        methods=["GET"],
        detail=False,
        url_path="response-codes",
    )
    def response_codes(self, *args, **kwargs):
        """Response Codes View"""
        return Response(
            export_response_codes(),
            status=status.HTTP_200_OK,
        )
