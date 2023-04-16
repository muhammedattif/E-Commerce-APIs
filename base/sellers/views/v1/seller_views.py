# REST Framework Imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# First Party Imports
from base.products.models import Product
from base.products.serializers.v1 import BestSellerProductSerializer, LowStockProductSerializer
from base.sellers.models import SellerInsight
from base.sellers.serializers.v1 import SalesChartSerializer
from base.users.authentication import CustomTokenAuthentication
from base.users.permissions import SellerPermission
from base.utility.response_codes import GeneralCodes


class SellerViewSet(viewsets.GenericViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [SellerPermission]

    @action(
        methods=["GET"],
        detail=False,
        url_path="sales-chart",
    )
    def sales_chart(self, *args, **kwargs):
        """Sales Chart View"""
        insights = SellerInsight(seller=self.request.user)
        serializer = SalesChartSerializer(insights.sales_chart(), many=True)
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["GET"],
        detail=False,
    )
    def insights(self, *args, **kwargs):
        """Insights View"""
        insights = SellerInsight(seller=self.request.user)
        best_seller_products_queryset = Product.objects.best_seller().filter(
            seller=self.request.user,
        )
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": {
                    "total_clicks": insights.total_clicks,
                    "clicks_today": insights.clicks_today,
                    "best_seller": BestSellerProductSerializer(best_seller_products_queryset, many=True).data,
                },
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["GET"],
        detail=False,
    )
    def inventory(self, *args, **kwargs):
        """Inventory View"""
        insights = SellerInsight(seller=self.request.user)
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "total_inventory": insights.total_inventory,
                "pending_items": insights.total_pending_inventory,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["GET"],
        detail=False,
    )
    def settlements(self, *args, **kwargs):
        """Settlements View"""
        insights = SellerInsight(seller=self.request.user)
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "total_sales": insights.total_sales_pending_settltment,
                "total_items": insights.total_items_pending_settlement,
                "total_sales_available_for_settelement": insights.total_sales_available_for_settlement,
                "total_items_available_for_settelement": insights.total_items_sold,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["GET"],
        detail=False,
        url_path="low-stock-products",
    )
    def low_stock_products(self, *args, **kwargs):
        """Low Stock Products View"""
        low_stock_queryset = (
            Product.objects.low_stock()
            .annotate_brand_name()
            .annotate_lowest_price()
            .filter(
                seller=self.request.user,
            )
        )
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": LowStockProductSerializer(low_stock_queryset, many=True).data,
            },
            status=status.HTTP_200_OK,
        )
