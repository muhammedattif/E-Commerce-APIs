# REST Framework Imports
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

# Other Third Party Imports
from django_filters.rest_framework import DjangoFilterBackend

# First Party Imports
from base.brands.model_filters import BrandFilter
from base.brands.models import Brand, BrandTracker
from base.brands.serializers import BrandDetailSerializer, BrandSerializer
from base.users.authentication import CustomTokenAuthentication, TokenOrAnonymousAuthentication
from base.users.models import Favorite
from base.users.permissions import BuyerPermission
from base.utility.response_codes import GeneralCodes


class BrandViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    authentication_classes = [TokenOrAnonymousAuthentication]
    permission_classes = []

    queryset = Brand.objects.filter(is_active=True).order_by("-id")
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BrandFilter
    search_fields = ["name"]

    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                {
                    "code": GeneralCodes.NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BrandDetailSerializer(instance, context={"request": request})
        BrandTracker.add(user=request.user, brand=instance)
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
        """Favorite a Brand"""
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                {
                    "code": GeneralCodes.NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        favorites, created = Favorite.objects.get_or_create(user=request.user)
        favorites.brands.add(instance)
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
        """Unfavorite a Brand"""

        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                {
                    "code": GeneralCodes.NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        favorites, created = Favorite.objects.get_or_create(user=request.user)
        favorites.brands.remove(instance)
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["GET"],
        detail=False,
        authentication_classes=[CustomTokenAuthentication],
        permission_classes=[BuyerPermission],
    )
    def favorites(self, request, *args, **kwargs):
        """Favorite Brands List"""

        favorites, created = Favorite.objects.get_or_create(user=request.user)
        brands_queryset = favorites.brands.filter(is_active=True)

        page = self.paginate_queryset(brands_queryset)
        serializer = BrandSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)
