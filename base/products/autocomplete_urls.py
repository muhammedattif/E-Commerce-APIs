# Django Imports
from django.urls import path

from .views import auto_complete

urlpatterns = [
    path(
        "product-options-autocomplete",
        auto_complete.ProductOptionsAutocompleteView.as_view(),
        name="product-options-autocomplete",
    ),
    path(
        "product-models-autocomplete",
        auto_complete.ProductModelsAutocompleteView.as_view(),
        name="product-models-autocomplete",
    ),
]
