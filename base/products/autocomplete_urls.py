# Django Imports
from django.urls import path

from .views import auto_complete

urlpatterns = [
    path(
        "product-options-autocomplete",
        auto_complete.ProductOptionsAutocompleteView.as_view(),
        name="product-options-autocomplete",
    ),
]
