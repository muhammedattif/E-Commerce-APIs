# Python Standard Library Imports

# Other Third Party Imports
from django_filters import rest_framework as filters


class AddressFilter(filters.FilterSet):
    is_primary = filters.BooleanFilter(field_name="is_primary", method="get_primary_addresses")

    @classmethod
    def get_primary_addresses(cls, queryset, name, value):
        """get a list of primary addresses"""
        if value:
            queryset = queryset.filter(
                is_primary=True,
                is_active=True,
            )
        return queryset
