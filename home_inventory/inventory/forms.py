from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit,
    Row,
    Layout,
    Fieldset,
    ButtonHolder,
    HTML,
    Column,
)
from dal import autocomplete
from django.forms import (
    ModelForm,
    DateInput,
    ModelChoiceField,
    CharField,
    NumberInput,
    Form,
)
from django.utils.translation import gettext_lazy as _
from .models import Item, Category, Product, Location


class LocationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "add-form"
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = Location
        fields = "__all__"


class ItemForm(ModelForm):

    category = ModelChoiceField(
        label=_("Category"),
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="category-autocomplete", attrs={"data-width": "100%"}
        ),
    )

    barcode = CharField(
        label=_("Barcode"), required=False, widget=NumberInput(attrs={"pattern": "\d*"})
    )

    class Meta:
        model = Item
        fields = "__all__"
        widgets = {
            "name": autocomplete.ModelSelect2(
                url="product-autocomplete", attrs={"data-width": "100%"}
            ),
            "expiry_date": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            ),
            # show numeric keyboard for both Android Chrome and iOS Safari
            "quantity": NumberInput(attrs={"pattern": "\d*"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "add-form"
        self.helper.form_class = "form-horizontal"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                "name",
                "barcode",
                "category",
                Row(
                    Column("quantity", css_class="form-group col-6 pe-1"),
                    Column("measurement", css_class="form-group col-6 ps-1"),
                ),
                "expiry_date",
                "location",
            ),
            ButtonHolder(
                Submit("submit", "Save"),
            ),
        )

    def save(self, commit=True):
        # assign category and barcode to product or change the existing one
        instance = super().save(commit=False)
        product_id = self.cleaned_data["name"].id
        category_id = self.cleaned_data["category"].id
        barcode = self.cleaned_data["barcode"]
        product = Product.objects.get(pk=product_id)

        if product.category is None or product.category.id != category_id:
            product.category = Category.objects.get(pk=category_id)
            product.save()

        if product.barcode is None or product.barcode != barcode:
            product.barcode = barcode
            product.save()

        if commit:
            instance.save()
        return instance


class AddItemForm(ItemForm):
    """Subclassed form when the item is added"""

    pass


class EditItemForm(ItemForm):
    """Subclassed form when the item is edited"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add Remove button
        self.helper.layout[1].append(
            HTML(
                """<input class="btn btn-danger" type="submit" value="Remove"
                    formaction="{% url 'delete-item' item_id=item.id %}">"""
            ),
        )


class SearchForm(Form):
    """Inputs for search"""

    name = CharField(label="Product name", max_length=200, required=False)
    barcode = CharField(label="Product barcode", max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "search-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                "name",
                "barcode",
            ),
            ButtonHolder(
                Submit("submit", "Search"),
            ),
        )

    def is_valid(self):
        """Return True if the form has no errors, or False otherwise."""
        basic_validation = super().is_valid()
        name = self.cleaned_data["name"]
        barcode = self.cleaned_data["barcode"]
        if name and barcode:  # can't search for both at the same time
            extra_validation = False
        elif name or barcode:  # but at least one value should be filled
            extra_validation = True
        else:
            extra_validation = False
        return basic_validation and extra_validation
