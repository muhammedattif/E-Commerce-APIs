# Django Imports
from django import forms

# Other Third Party Imports
from dal import autocomplete

# First Party Imports
from base.products.models import Model


class CartItemForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = "__all__"
        widgets = {
            "model": autocomplete.ModelSelect2Multiple(
                url="product-models-autocomplete",
                forward=["product"],
            ),
        }
