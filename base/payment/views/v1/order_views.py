# REST Framework Imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# First Party Imports
from base.payment.models import Order
from base.payment.serializers.v1 import OrderDetailSerializer, OrderSerializer, OrderTrackerSerializer
from base.users.authentication import CustomTokenAuthentication
from base.users.permissions import BuyerPermission
from base.utility.classes import Requests
from base.utility.response_codes import GeneralCodes, PaymentCodes


class OrderViewSet(viewsets.GenericViewSet):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [BuyerPermission]

    queryset = Order.objects.order_by("-created_at")
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        context = {"request": self.request, "lang": Requests.get_language(self.request)}
        self.serializer_class.context = context
        return self.serializer_class

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def list(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
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

        serializer = OrderDetailSerializer(instance, context={"request": request})
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=True,
    )
    def cancel(self, *args, **kwargs):
        pk = kwargs.get("pk")
        order = self.get_queryset().filter(pk=pk).first()
        if not order:
            return Response({"code": GeneralCodes.INVALID_DATA}, status=status.HTTP_400_BAD_REQUEST)

        is_cancelled = order.cancel()
        if not is_cancelled:
            return Response({"code": PaymentCodes.CANNOT_CANCEL_ORDER}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"code": GeneralCodes.SUCCESS}, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
    )
    def tracking(self, *args, **kwargs):
        pk = kwargs.get("pk")
        order = self.get_queryset().filter(pk=pk).first()
        if not order:
            return Response({"code": GeneralCodes.INVALID_DATA}, status=status.HTTP_400_BAD_REQUEST)

        order_tracking = order.tracker.all().order_by("created_at")
        serializer = OrderTrackerSerializer(order_tracking, many=True)
        return Response({"code": GeneralCodes.SUCCESS, "data": serializer.data}, status=status.HTTP_200_OK)
