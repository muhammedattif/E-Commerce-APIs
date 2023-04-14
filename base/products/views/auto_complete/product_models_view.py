# Django Imports
from django.db.models import Q

# Other Third Party Imports
from dal import autocomplete

# First Party Imports
from base.products.models import Model
from base.users.permissions import StafUserPermissiondMixin


class ProductModelsAutocompleteView(StafUserPermissiondMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        product = self.forwarded.get("product")
        qs = Model.objects.all()
        if not product:
            return qs.none()

        qs = qs.filter(
            product__id=product,
        )

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))
        return qs
