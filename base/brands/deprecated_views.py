# REST Framework Imports
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .deprecated_models import Brand, CustomerBagItem, CustomerFavoriteBrand, CustomerFavoriteItem, HomePageSection
from .deprecated_serializers import (
    BrandPageSerializer,
    BrandSerializer,
    CustomerBagItemSerializer,
    CustomerFavoriteBrandSerializer,
    CustomerFavoriteItemSerializer,
    HomePageSectionSerializer,
)

# Create your views here.


class BrandPageView(generics.RetrieveAPIView):
    serializer_class = BrandPageSerializer
    queryset = Brand.objects.all()
    permission_classes = [AllowAny]


class AllBrandsView(generics.ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    permission_classes = [AllowAny]


class AddCustomerBagItemView(generics.CreateAPIView):
    serializer_class = CustomerBagItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data["customer"] = request.user.customer.pk
        request.data["item"] = self.kwargs.get("item")
        return super().post(request, *args, **kwargs)


class AddCustomerFavoriteBrandView(generics.CreateAPIView):
    serializer_class = CustomerFavoriteBrandSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data["customer"] = request.user.customer.pk
        request.data["brand"] = self.kwargs.get("brand")
        return super().post(request, *args, **kwargs)


class AddCustomerFavoriteItemView(generics.CreateAPIView):
    serializer_class = CustomerFavoriteItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data["customer"] = request.user.customer.pk
        request.data["item"] = self.kwargs.get("item")
        return super().post(request, *args, **kwargs)


class RemoveCustomerBagItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "item"

    def get_queryset(self):
        return CustomerBagItem.objects.filter(customer__user=self.request.user)


class RemoveCustomerFavoriteBrandView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "brand"

    def get_queryset(self):
        return CustomerFavoriteBrand.objects.filter(customer__user=self.request.user)


class RemoveCustomerFavoriteItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "item"

    def get_queryset(self):
        return CustomerFavoriteItem.objects.filter(customer__user=self.request.user)


class ListCustomerBagItemsView(generics.ListAPIView):
    serializer_class = CustomerBagItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerBagItem.objects.filter(customer__user=self.request.user)


class ListCustomerFavoriteBrandsView(generics.ListAPIView):
    serializer_class = CustomerFavoriteBrandSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerFavoriteBrand.objects.filter(customer__user=self.request.user)


class ListCustomerFavoriteItemsView(generics.ListAPIView):
    serializer_class = CustomerFavoriteItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerFavoriteItem.objects.filter(customer__user=self.request.user)


class ListHomePageSectionsView(generics.ListAPIView):
    serializer_class = HomePageSectionSerializer
    permission_classes = [AllowAny]
    queryset = HomePageSection.objects.filter(show_on_home_page=True).order_by("order")
