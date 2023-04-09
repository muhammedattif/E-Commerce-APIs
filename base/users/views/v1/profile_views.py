# Django Imports

# REST Framework Imports
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

# First Party Imports
from base.users.serializers import UserSerializer
from base.utility.response_codes import GeneralCodes


class ProfileViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):

        serializer = UserSerializer(request.user, many=False)
        return Response({"code": GeneralCodes.SUCCESS, "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Update Profile"""

        serializer = UserSerializer(
            data=request.data,
            instance=request.user,
        )
        if not serializer.is_valid():
            return Response(
                {
                    "code": serializer.code,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response({"code": GeneralCodes.SUCCESS, "data": serializer.data}, status=status.HTTP_200_OK)
