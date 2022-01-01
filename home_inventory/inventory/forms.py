from django.forms import ModelForm, DateInput
from .models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ("location",)

        widgets = {
            "expiry_date": DateInput(
                format=("%d-%m-%Y"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            ),
        }
