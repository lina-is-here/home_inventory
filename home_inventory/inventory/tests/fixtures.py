import pytest

from ..models import Product, Location, Measurement, Category


@pytest.fixture()
def created_product(db):
    product = Product.objects.create(name="Product name")
    yield product


@pytest.fixture()
def created_category(db):
    category = Category.objects.create(name="Category name")
    yield category


@pytest.fixture()
def created_location(db):
    location = Location.objects.create(name="Location name")
    yield location


@pytest.fixture()
def created_measurement(db):
    measurement = Measurement.objects.create(name="Measurement name")
    yield measurement
