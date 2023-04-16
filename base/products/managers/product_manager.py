# Django Imports
from django.db import models
from django.db.models import Count, F, IntegerField, OuterRef, Q, Subquery, Sum
from django.db.models.functions import Coalesce

# First Party Imports
from base.payment.utils.choices import OrderItemStatusChoices


class ProductQuerySet(models.QuerySet):
    def popular(self):
        return self.annotate_total_clicks().order_by("-total_clicks")

    def annotate_total_clicks(self):
        return self.annotate(
            total_clicks=Coalesce(
                Count("trackers"),
                0,
                output_field=IntegerField(),
            ),
        )

    def annotate_total_sold(self):
        return self.annotate(
            total_sold=Coalesce(
                Sum(
                    F("models__order_items__quantity") - F("models__order_items__quantity_refunded"),
                    filter=Q(
                        models__order_items__status__in=[
                            OrderItemStatusChoices.PAID,
                            OrderItemStatusChoices.REFUNDED,
                        ],
                    ),
                ),
                0,
                output_field=IntegerField(),
            ),
        )

    def annotate_total_inventory(self):
        return self.annotate(
            total_inventory=Coalesce(
                Sum("models__inventory_quantity"),
                0,
                output_field=IntegerField(),
            ),
        )

    def annotate_lowest_price(self):
        # First Party Imports
        from base.products.models import Model

        lowest_price = Subquery(
            Model.objects.filter(
                product=OuterRef("id"),
            )
            .order_by("price")
            .values("price")[:1],
        )
        return self.annotate(
            price=lowest_price,
        )

    def annotate_brand_name(self):
        # First Party Imports
        from base.brands.models import Brand

        brand_name = Subquery(
            Brand.objects.filter(
                seller__products__in=OuterRef("id"),
            )
            .order_by("-created_at")
            .values("name")[:1],
        )
        return self.annotate(
            brand_name=brand_name,
        )

    def low_stock(self):
        return (
            self.annotate_total_inventory()
            .filter(
                total_inventory__lt=5,
            )
            .order_by(
                "-total_inventory",
            )
        )

    def best_seller(self):
        return (
            self.annotate_total_clicks()
            .annotate_total_inventory()
            .annotate_total_sold()
            .exclude(
                total_sold=0,
            )
            .order_by(
                "-total_clicks",
                "-total_inventory",
                "-total_sold",
            )
        )


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def popular(self):
        return self.get_queryset().popular()

    def low_stock(self):
        return self.get_queryset().low_stock()

    def best_seller(self):
        return self.get_queryset().best_seller()

    def annotate_lowest_price(self):
        return self.get_queryset().annotate_lowest_price()

    def annotate_brand_name(self):
        return self.get_queryset().annotate_brand_name()

    def annotate_total_clicks(self):
        return self.get_queryset().annotate_total_clicks()

    def annotate_total_sold(self):
        return self.get_queryset().annotate_total_sold()

    def annotate_total_inventory(self):
        return self.get_queryset().annotate_total_inventory()
