# Django Imports
from django.db import models
from django.db.models import IntegerField, OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce


class ProductQuerySet(models.QuerySet):
    def popular(self):
        return self.annotate(
            clicks=Coalesce(
                Sum("trackers__clicks"),
                0,
                output_field=IntegerField(),
            ),
        ).order_by("-clicks")

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


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def popular(self):
        return self.get_queryset().popular()

    def annotate_lowest_price(self):
        return self.get_queryset().annotate_lowest_price()

    def annotate_brand_name(self):
        return self.get_queryset().annotate_brand_name()
