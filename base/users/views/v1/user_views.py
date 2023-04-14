# REST Framework Imports
from rest_framework import viewsets
from rest_framework.decorators import action

# First Party Imports
from base.products.serializers.v1 import ProductSerializer
from base.users.authentication import CustomTokenAuthentication
from base.users.models import Favorite
from base.users.permissions import BuyerPermission


class UserViewSet(viewsets.GenericViewSet):
    @action(
        methods=["GET"],
        detail=False,
        authentication_classes=[CustomTokenAuthentication],
        permission_classes=[BuyerPermission],
    )
    def whishlist(self, request, *args, **kwargs):
        """User's Wishlist"""

        favorites, created = Favorite.objects.get_or_create(user=request.user)
        products_queryset = favorites.products.filter(is_active=True, is_approved=True)

        page = self.paginate_queryset(products_queryset)
        serializer = ProductSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)
