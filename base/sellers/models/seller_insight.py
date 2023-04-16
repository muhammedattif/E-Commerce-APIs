# Django Imports
from django.db.models import F, FloatField, IntegerField, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

# First Party Imports
from base.payment.models import OrderItem
from base.payment.utils.choices import OrderItemStatusChoices
from base.products.models import Model, Product, ProductApproval, ProductTracker
from base.sellers.models import InventoryRequest
from base.sellers.utils.choices import InventoryRequestStatusChoices, InventoryRequestTypesChoices


class SellerInsight:
    def __init__(self, seller) -> None:
        self.seller = seller
        self.models_queryset = Model.objects.filter(product__seller=self.seller)
        self.items_pending_settlement_queryset = self.models_queryset.filter(
            order_items__status__in=[
                OrderItemStatusChoices.INITIATED,
                OrderItemStatusChoices.CONFIRMED,
            ],
        )
        self.items_sold_queryset = self.models_queryset.filter(
            order_items__status__in=[
                OrderItemStatusChoices.PAID,
                OrderItemStatusChoices.REFUNDED,
            ],
        )
        self.products_clicks_queryset = ProductTracker.objects.filter(product__seller=self.seller)
        self.inventory_requests_queryset = InventoryRequest.objects.filter(seller=self.seller)
        self.products_queryset = Product.objects.filter(seller=self.seller)
        self.product_approval_queryset = ProductApproval.objects.filter(seller=self.seller)
        self.order_items_queryset = OrderItem.objects.filter(product__seller=self.seller)

    @property
    def total_models(self):
        return self.models_queryset.count()

    def models_pending_approval_queryset(self):
        return self.product_approval_queryset.count()

    @property
    def total_clicks(self):
        return self.products_clicks_queryset.count()

    @property
    def clicks_today(self):
        return self.products_clicks_queryset.filter(created_at__date=timezone.now().today()).count()

    @property
    def total_inventory(self):
        return self.models_queryset.aggregate(
            sum=Coalesce(
                Sum("inventory_quantity"),
                0,
                output_field=IntegerField(),
            ),
        )["sum"]

    @property
    def total_pending_inventory(self):
        return self.inventory_requests_queryset.filter(
            type=InventoryRequestTypesChoices.ADD,
            status=InventoryRequestStatusChoices.SUBMITTED,
        ).aggregate(
            sum=Coalesce(
                Sum("quantity"),
                0,
                output_field=IntegerField(),
            ),
        )[
            "sum"
        ]

    def sales_chart(self):
        return (
            self.order_items_queryset.filter(
                status__in=[
                    OrderItemStatusChoices.PAID,
                    OrderItemStatusChoices.REFUNDED,
                ],
            )
            .values(
                "created_at",
            )
            .annotate(
                total_sales=Coalesce(
                    Sum(F("price") * (F("quantity") - F("quantity_refunded"))),
                    0,
                    output_field=FloatField(),
                ),
                total_items_sold=Sum((F("quantity") - F("quantity_refunded"))),
            )
            .order_by(
                "created_at",
            )
        )

    @property
    def total_items_pending_settlement(self):
        return self.items_pending_settlement_queryset.aggregate(
            total_pending_settlement=Coalesce(
                Sum(F("order_items__quantity") - F("order_items__quantity_refunded")),
                0,
                output_field=IntegerField(),
            ),
        )["total_pending_settlement"]

    @property
    def total_sales_pending_settltment(self):
        return self.items_pending_settlement_queryset.aggregate(
            total_sales=Coalesce(
                Sum(F("order_items__price") * (F("order_items__quantity") - F("order_items__quantity_refunded"))),
                0,
                output_field=IntegerField(),
            ),
        )["total_sales"]

    @property
    def total_items_sold(self):
        return self.items_sold_queryset.aggregate(
            total_sold=Coalesce(
                Sum(F("order_items__quantity") - F("order_items__quantity_refunded")),
                0,
                output_field=IntegerField(),
            ),
        )["total_sold"]

    @property
    def total_sales_available_for_settltment(self):
        return self.items_sold_queryset.aggregate(
            total_sales=Coalesce(
                Sum(F("order_items__price") * (F("order_items__quantity") - F("order_items__quantity_refunded"))),
                0,
                output_field=IntegerField(),
            ),
        )["total_sales"]
