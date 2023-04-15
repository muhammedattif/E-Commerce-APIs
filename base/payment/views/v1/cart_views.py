# Django Imports
from django.db import transaction

# REST Framework Imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# First Party Imports
from base.payment.models import Cart, CartItem, Order, OrderItem
from base.payment.serializers.v1 import (
    AddToCartInputerializer,
    CartSerializer,
    CheckoutInputSerializer,
    OrderSerializer,
    UpdateCartItemInputerializer,
)
from base.users.authentication import CustomTokenAuthentication
from base.users.permissions import BuyerPermission
from base.utility.classes import Requests
from base.utility.response_codes import GeneralCodes, PaymentCodes, ProductsCodes


class CartViewSet(viewsets.GenericViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [BuyerPermission]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def list(self, *args, **kwargs):
        cart = self.get_object()
        serializer = CartSerializer(cart, many=False, context={"request": self.request})
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=False,
    )
    def clear(self, *args, **kwargs):
        """Add Product to Cart"""
        self.get_object().clear()
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=False,
    )
    def add(self, request, *args, **kwargs):
        """Add Product to Cart"""

        input_serializer = AddToCartInputerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(
                {
                    "code": input_serializer.code,
                    "errors": input_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = input_serializer.validated_data.get("product")
        model = input_serializer.validated_data.get("model")
        quantity = input_serializer.validated_data.get("quantity")
        cart = self.get_object()

        product_in_cart = cart.items.filter(
            product=product,
            model=model,
        ).first()

        quantity_in_cart = getattr(product_in_cart, "quantity", 0)
        total_quantity = quantity + quantity_in_cart
        if not model.is_available_in_inventory(quantity=total_quantity):
            return Response(
                {
                    "code": ProductsCodes.QUANTITY_UNAVAILBLE,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if product_in_cart:
            product_in_cart.quantity = total_quantity
            product_in_cart.save()
        else:
            CartItem.objects.create(
                cart=cart,
                product=product,
                model=model,
                quantity=total_quantity,
            )

        return Response(
            {
                "code": GeneralCodes.SUCCESS,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=False,
        url_path=r"items/(?P<pk>[^/.]+)/remove",
    )
    def remove(self, *args, **kwargs):
        """Remove Product from Cart"""
        pk = kwargs.get("pk")
        cart = self.get_object()
        cart_item = cart.items.filter(id=pk).first()
        if not cart_item:
            return Response(
                {
                    "code": GeneralCodes.INVALID_DATA,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        cart_item.delete()
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["PUT"],
        detail=False,
        url_path=r"items/(?P<pk>[^/.]+)/update",
    )
    def update_quantity(self, *args, **kwargs):
        """Update Product from Cart"""

        input_serializer = UpdateCartItemInputerializer(data=self.request.data)
        if not input_serializer.is_valid():
            return Response(
                {
                    "code": input_serializer.code,
                    "errors": input_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        quantity = input_serializer.validated_data.get("quantity")
        pk = kwargs.get("pk")
        cart = self.get_object()

        cart_item = (
            cart.items.select_related("model")
            .filter(
                id=pk,
            )
            .first()
        )
        if not cart_item:
            return Response(
                {
                    "code": GeneralCodes.INVALID_DATA,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not cart_item.model.is_available_in_inventory(quantity=quantity):
            return Response(
                {
                    "code": ProductsCodes.QUANTITY_UNAVAILBLE,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item.quantity = quantity
        cart_item.save()

        return Response(
            {
                "code": GeneralCodes.SUCCESS,
            },
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    @action(
        methods=["POST"],
        detail=False,
    )
    def checkout(self, *args, **kwargs):

        input_serializer = CheckoutInputSerializer(
            data=self.request.data,
            context={"request": self.request},
        )
        if not input_serializer.is_valid():
            return Response(
                {
                    "code": input_serializer.code,
                    "errors": input_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        address = input_serializer.address
        cart, created = Cart.objects.get_or_create(user=self.request.user)

        # Get cart items
        cart_items = cart.items.select_related("model", "product")
        if not cart_items:
            return Response({"code": PaymentCodes.EMPTY_CART}, status=status.HTTP_400_BAD_REQUEST)

        # Check if all items quantity available
        # Cart items may be added for a long time
        for item in cart_items:

            if item.model.is_out_of_stock:
                response = {
                    "code": ProductsCodes.OUT_OF_STOCK,
                    "product_name": item.product.name,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            elif not item.is_available_in_inventory:
                response = {
                    "code": ProductsCodes.QUANTITY_UNAVAILBLE,
                    "product_name": item.product.name,
                    "available_quantity": item.model.inventory_quantity,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=self.request.user,
            total=cart.total,
            sub_total=cart.sub_total,
            discount=cart.discount,
            taxes=cart.taxes,
            address=address,
        )
        for item in cart_items:
            OrderItem.objects.create(
                product=item.product,
                order=order,
                model=item.model,
                price=item.model.price,
                quantity=item.quantity,
            )

        serializer = OrderSerializer(order, many=False, context={"lang": Requests.get_language(self.request)})
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
