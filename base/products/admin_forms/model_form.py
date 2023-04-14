# Django Imports
from django import forms

# Other Third Party Imports
from dal import autocomplete

# First Party Imports
from base.products.models import Model


class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = "__all__"
        widgets = {
            "product_options": autocomplete.ModelSelect2Multiple(
                url="product-options-autocomplete",
                forward=["product"],
            ),
        }
