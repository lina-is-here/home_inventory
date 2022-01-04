from dal import autocomplete
from django.forms import ModelForm, DateInput, ModelChoiceField
from django.utils.translation import gettext, gettext_lazy as _
from .models import Item, Category, Product, Location


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = "__all__"


class ItemForm(ModelForm):

    category = ModelChoiceField(
        label=_("Category"),
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url="category-autocomplete"),
    )

    class Meta:
        model = Item
        fields = "__all__"
        widgets = {
            "name": autocomplete.ModelSelect2(
                url="product-autocomplete"
            ),
            "expiry_date": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            ),
        }

    def save(self, commit=True):
        # assign category to product or change the existing one
        instance = super().save(commit=False)
        product_id = self.cleaned_data["name"].id
        category_id = self.cleaned_data["category"].id
        product = Product.objects.get(pk=product_id)

        if product.category is None or product.category.id != category_id:
            product.category = Category.objects.get(pk=category_id)
            product.save()
        if commit:
            instance.save()
        return instance
