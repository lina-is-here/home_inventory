from dal import autocomplete
from django.forms import ModelForm, DateInput
from .models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        widgets = {
            "name": autocomplete.ModelSelect2(url="product-autocomplete"),
            "expiry_date": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            ),
        }
