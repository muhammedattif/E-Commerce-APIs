# REST Framework Imports
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

# Other Third Party Imports
from django_filters.rest_framework import DjangoFilterBackend

# First Party Imports
from base.products.model_filters import ProductFilter
from base.products.models import Product, ProductTracker
from base.products.serializers.v1 import ProductAvailabilityInputSerializer, ProductDetailSerializer, ProductSerializer
from base.products.utils.choices import InventoryStatuses
from base.users.authentication import CustomTokenAuthentication
from base.users.models import Favorite
from base.users.permissions import BuyerPermission
from base.utility.response_codes import GeneralCodes, ProductsCodes


class ProductViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    authentication_classes = []
    permission_classes = []

    queryset = (
        Product.objects.annotate_brand_name()
        .annotate_lowest_price()
        .filter(
            is_approved=True,
            is_active=True,
        )
        .order_by("-created_at")
        .distinct()
    )
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "about"]
    filterset_fields = ["name"]
    ordering_fields = ["models__price", "created_at"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                {
                    "code": GeneralCodes.NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductDetailSerializer(instance, context={"request": request})
        ProductTracker.add(user=request.user, product=instance)
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
        authentication_classes=[CustomTokenAuthentication],
        permission_classes=[BuyerPermission],
    )
    def favorite(self, request, pk, *args, **kwargs):
        """Add a Product to Favorites"""
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                {
                    "code": GeneralCodes.NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        favorites, created = Favorite.objects.get_or_create(user=request.user)
        favorites.products.add(instance)
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=True,
        authentication_classes=[CustomTokenAuthentication],
        permission_classes=[BuyerPermission],
    )
    def unfavorite(self, request, pk, *args, **kwargs):
        """Remove a Product to Favorites"""
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                {
                    "code": GeneralCodes.NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        favorites, created = Favorite.objects.get_or_create(user=request.user)
        favorites.products.remove(instance)
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="availability-check",
        authentication_classes=[CustomTokenAuthentication],
        permission_classes=[BuyerPermission],
    )
    def availability_check(self, request, pk, *args, **kwargs):
        """Product's Availability Check"""

        instance = self.get_queryset().prefetch_related("models").filter(pk=pk).first()
        if not instance:
            return Response(
                {
                    "code": GeneralCodes.NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        input_serializer = ProductAvailabilityInputSerializer(
            data=request.data,
        )
        if not input_serializer.is_valid():
            return Response(
                {
                    "code": input_serializer.code,
                    "errors": input_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        options = input_serializer.validated_data.get("options")
        quantity = input_serializer.validated_data.get("quantity")

        model, inventory_status = instance.check_inventory(
            options=options,
            quantity=quantity,
        )

        if inventory_status == InventoryStatuses.NOT_AVAILBLE:
            return Response({"code": ProductsCodes.NOT_AVAILBLE}, status=status.HTTP_400_BAD_REQUEST)
        elif inventory_status == InventoryStatuses.OUT_OF_STOCK:
            return Response({"code": ProductsCodes.OUT_OF_STOCK}, status=status.HTTP_400_BAD_REQUEST)
        elif inventory_status == InventoryStatuses.QUANTITY_UNAVAILBLE:
            return Response({"code": ProductsCodes.QUANTITY_UNAVAILBLE}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "code": ProductsCodes.AVAILABLE,
                "model": model.id,
                "price": model.price,
                "total_price": model.price * quantity,
            },
            status=status.HTTP_200_OK,
        )
