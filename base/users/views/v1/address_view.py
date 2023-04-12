# Django Imports

# REST Framework Imports
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

# Other Third Party Imports
from django_filters.rest_framework import DjangoFilterBackend

# First Party Imports
from base.users.model_filters import AddressFilter
from base.users.models import Address
from base.users.serializers import AddressCreateSerialiser, AddressSerialiser, AddressUpdateSerialiser
from base.utility.response_codes import GeneralCodes


class AddressViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Address.objects.filter(is_active=True).order_by("-id")
    serializer_class = AddressSerialiser
    filter_backends = [DjangoFilterBackend]
    filterset_class = AddressFilter

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                user=self.request.user,
            )
            .order_by("-is_primary")
        )

    def create(self, request, *args, **kwargs):
        serializer = AddressCreateSerialiser(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "code": serializer.code,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        address = Address.objects.create(user=request.user, **serializer.validated_data)

        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": AddressSerialiser(address).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                {
                    "code": GeneralCodes.NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(instance, context={"request": request})
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, pk, *args, **kwargs):
        """Update address"""

        instance = (
            self.get_queryset()
            .filter(
                pk=pk,
            )
            .first()
        )
        if not instance:
            return Response(
                {
                    "code": GeneralCodes.NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AddressUpdateSerialiser(
            data=request.data,
            instance=instance,
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
