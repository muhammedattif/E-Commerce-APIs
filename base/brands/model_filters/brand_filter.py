# Python Standard Library Imports

# Other Third Party Imports
from django_filters import rest_framework as filters


class BrandFilter(filters.FilterSet):
    is_popular = filters.BooleanFilter(field_name="is_popular", method="get_popular_brands")

    @classmethod
    def get_popular_brands(cls, queryset, name, value):
        """get a list of popular brands"""
        if value:
            queryset = queryset.popular().filter(
                is_active=True,
            )
        return queryset
