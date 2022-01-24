import pytest

from .fixtures import (
    created_product,
    created_location,
    created_measurement,
    created_category,
)
from ..forms import LocationForm, ItemForm, EditItemForm
from ..models import Product, Category, Item

pytestmark = pytest.mark.django_db


class TestLocationForm:
    def test_location(self):
        form = LocationForm(data={"name": "Fridge"})
        assert form.is_valid()


class TestItemForm:
    def test_item(
        self, created_product, created_location, created_measurement, created_category
    ):
        form = ItemForm(
            data={
                "name": created_product,
                "location": created_location,
                "quantity": 1,
                "measurement": created_measurement,
                "category": created_category,
            }
        )
        assert form.is_valid()

    def test_save(self, created_category, created_location, created_measurement):
        product = Product.objects.create(name="New product", category=created_category)

        new_category = Category.objects.create(name="new category")
        form = ItemForm(
            data={
                "name": product,
                "location": created_location,
                "quantity": 1,
                "measurement": created_measurement,
                "category": new_category,
                "barcode": "123456789",
            }
        )
        assert form.is_valid()
        form.save()
        saved_product = Product.objects.get(id=product.id)
        # product gets updated category and barcode
        assert saved_product.category.name == "new category"
        assert saved_product.barcode == "123456789"


class TestAddItemForm:
    pass


class TestEditItemForm:
    def test_edit_item(
        self, created_product, created_category, created_location, created_measurement
    ):
        item = Item.objects.create(
            name=created_product,
            location=created_location,
            measurement=created_measurement,
        )
        form = EditItemForm(
            data={
                "name": created_product,
                "location": created_location,
                "quantity": 5,
                "measurement": created_measurement,
                "category": created_category,
            }
        )
        assert form.is_valid()
        item = form.save()
        assert item.quantity == 5
