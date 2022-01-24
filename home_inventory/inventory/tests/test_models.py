import datetime
from random import choice
from string import printable

import pytest
from django.db import IntegrityError
from slugify import slugify

from .fixtures import created_product, created_location, created_measurement
from ..models import Category, Product, Location, Measurement, Item

pytestmark = pytest.mark.django_db


class TestCategory:
    # 200 characters limit
    category_name = "".join(choice(printable) for i in range(200))

    def test_save(self):
        category = Category.objects.create(name=self.category_name)
        assert category.name == self.category_name
        # check slugify_name is created for the 200 characters string as well
        assert category.slugify_name == slugify(self.category_name)

    def test___str__(self):
        category = Category.objects.create(name=self.category_name)
        assert category.__str__() == self.category_name


class TestProduct:
    # 200 characters limit
    product_name = "".join(choice(printable) for i in range(200))

    def test_save(self):
        product = Product.objects.create(name=self.product_name)
        assert product.name == self.product_name
        # check slugify_name is created for the 200 characters string as well
        assert product.slugify_name == slugify(self.product_name)
        assert product.barcode is None

    def test___str__(self):
        product = Product.objects.create(name=self.product_name)
        assert product.__str__() == self.product_name


class TestLocation:
    # 200 characters limit
    location_name = "".join(choice(printable) for i in range(200))

    def test_get_absolute_url(self):
        location = Location.objects.create(name=self.location_name)
        assert location.get_absolute_url() == f"/locations/{location.id}/"

    def test___str__(self):
        location = Location.objects.create(name=self.location_name)
        assert location.__str__() == self.location_name


class TestMeasurement:
    # 100 characters limit
    measurement_name = "".join(choice(printable) for i in range(100))

    def test_is_default_value(self):
        measurement = Measurement.objects.create(name=self.measurement_name)
        assert measurement.is_default is False

    def test_unique_constraint(self):
        Measurement.objects.create(name=self.measurement_name, is_default=True)
        with pytest.raises(IntegrityError):
            Measurement.objects.create(name=self.measurement_name, is_default=True)

    def test___str__(self):
        measurement = Measurement.objects.create(name=self.measurement_name)
        assert measurement.__str__() == self.measurement_name


class TestItem:
    def test_expired_item(self, created_product, created_location, created_measurement):
        item = Item.objects.create(
            name=created_product,
            location=created_location,
            measurement=created_measurement,
            # yesterday
            expiry_date=datetime.date.today() - datetime.timedelta(days=1),
        )
        assert item.is_expired is True
        assert item.is_expiring_soon is False

    def test_expiring_soon_item(
        self, created_product, created_location, created_measurement
    ):
        item = Item.objects.create(
            name=created_product,
            location=created_location,
            measurement=created_measurement,
            # today
            expiry_date=datetime.date.today(),
        )
        assert item.is_expired is False
        assert item.is_expiring_soon is True

    def test_not_expired_not_expiring_item(
        self, created_product, created_location, created_measurement
    ):
        item = Item.objects.create(
            name=created_product,
            location=created_location,
            measurement=created_measurement,
            # today + 7 days
            expiry_date=datetime.date.today() + datetime.timedelta(days=7),
        )
        assert item.is_expired is False
        assert item.is_expiring_soon is False

    def test___str__(self, created_product, created_location, created_measurement):
        item = Item.objects.create(
            name=created_product,
            location=created_location,
            measurement=created_measurement,
        )
        assert item.__str__() == created_product.name
