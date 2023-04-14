# Django Imports
from django.db.models import Q

# Other Third Party Imports
from dal import autocomplete

# First Party Imports
from base.products.models import ProductOption
from base.users.permissions import StafUserPermissiondMixin


class ProductOptionsAutocompleteView(StafUserPermissiondMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        product = self.forwarded.get("product")
        qs = ProductOption.objects.all()
        if not product:
            return qs.none()

        qs = qs.filter(
            product_feature__product__id=product,
        )

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))
        return qs
