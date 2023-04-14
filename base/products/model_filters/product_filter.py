# Python Standard Library Imports
from functools import reduce

# Django Imports
from django.db.models import Q

# Other Third Party Imports
from django_filters import rest_framework as filters


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    is_popular = filters.BooleanFilter(field_name="is_popular", method="get_popular_products")
    category__in = CharInFilter(field_name="category__id", lookup_expr="in")
    brand__in = CharInFilter(field_name="seller__brands__id", lookup_expr="in")
    price = filters.RangeFilter(field_name="models__price")
    price_low_to_high = filters.BooleanFilter(field_name="price_low_to_high", method="get_popular_products")
    price_high_to_low = filters.BooleanFilter(field_name="price_high_to_low", method="get_popular_products")
    # ordering = filters.OrderingFilter(
    #     # tuple-mapping retains order
    #     fields=(
    #         ('models__price', 'price'),
    #         ('created_at', 'created_at'),
    #     ),
    #     distinct=True
    # )
    color__in = CharInFilter(field_name="colors", method="get_colors")
    size__in = CharInFilter(field_name="sizes", method="get_sizes")

    @classmethod
    def get_popular_products(cls, queryset, name, value):
        """get a list of popular products"""
        if value:
            queryset = queryset.popular().filter(
                is_active=True,
            )
        return queryset

    @classmethod
    def get_colors(cls, queryset, name, value):
        """get a list of colored products"""
        if value:
            q_list = map(lambda n: Q(features__options__name__iexact=n), value)
            q_list = reduce(lambda a, b: a | b, q_list)
            queryset = queryset.filter(
                q_list,
                features__name__iexact="color",
            )
        return queryset

    @classmethod
    def get_sizes(cls, queryset, name, value):
        """get a list of sized products"""
        if value:
            q_list = map(lambda n: Q(features__options__name__iexact=n), value)
            q_list = reduce(lambda a, b: a | b, q_list)
            queryset = queryset.filter(
                q_list,
                features__name__iexact="size",
            )
        return queryset
