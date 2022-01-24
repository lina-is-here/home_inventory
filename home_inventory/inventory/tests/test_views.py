import json
from unittest.mock import MagicMock

import pytest

from .fixtures import (
    created_product,
    created_category,
    created_location,
    created_measurement,
)
from ..models import Item

from ..views import (
    CustomComplete,
    ProductAutoComplete,
    CategoryAutoComplete,
    get_product,
    get_product_by_barcode,
    get_location_context,
    get_index_context,
    index,
    location_detail,
    add_location,
    add_item,
    edit_item,
    delete_item,
)


class TestCustomComplete:
    def test_create_option_not_displayed(self):
        cc = CustomComplete(create_field=True)
        context = MagicMock()
        q = "query"
        assert cc.get_create_option(context, q) == []

    def test_create_option_not_displayed_slugified(self):
        cc = CustomComplete(create_field=True)
        # list of existing options
        d = {"object_list": ["QUERY-1"]}
        context = MagicMock()
        context.__getitem__.side_effect = d.__getitem__
        q = "query 1"
        assert cc.get_create_option(context, q) == []

    def test_create_option_is_displayed(self):
        cc = CustomComplete(create_field=True)
        cc.get_queryset = MagicMock()
        cc.request = MagicMock()
        context = MagicMock()
        context.get.return_value = None
        q = "query 1"
        assert cc.get_create_option(context, q) == [
            {"id": "query 1", "text": 'Create "query 1"', "create_id": True}
        ]


class TestProductAutoComplete:
    def test_has_add_permission(self):
        request = MagicMock()
        pac = ProductAutoComplete()
        assert pac.has_add_permission(request) is True

    def test_get_queryset(self, db):
        pac = ProductAutoComplete(q="Query 1")
        qs = pac.get_queryset()
        assert [item.name for item in qs] == []

    def test_get_queryset_value(self, db, created_product):
        pac = ProductAutoComplete(q=created_product.name.lower()[:4])
        qs = pac.get_queryset()
        assert [item.name for item in qs] == [created_product.name]


class TestCategoryAutoComplete:
    def test_has_add_permission(self):
        request = MagicMock()
        cac = CategoryAutoComplete()
        assert cac.has_add_permission(request) is True

    def test_get_queryset(self, db):
        cac = CategoryAutoComplete(q="Query 1")
        qs = cac.get_queryset()
        assert [item.name for item in qs] == []

    def test_get_queryset_value(self, db, created_category):
        cac = CategoryAutoComplete(q=created_category.name.lower()[:4])
        qs = cac.get_queryset()
        assert [item.name for item in qs] == [created_category.name]


def test_get_product(db, created_product, created_category):
    created_product.category = created_category
    created_product.save()
    response = get_product("", created_product.name)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "category_id": created_category.id,
        "category_name": created_category.name,
        "barcode": created_product.barcode,
    }


def test_get_product_by_barcode_exists(db, created_product):
    created_product.barcode = "12345"
    created_product.save()
    response = get_product_by_barcode("", "12345")
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "id": created_product.id,
        "name": created_product.name,
    }


def test_get_product_by_barcode_not_exists(db, created_product):
    created_product.barcode = "12345"
    created_product.save()
    response = get_product_by_barcode("", "11111")
    assert response.status_code == 200
    assert response.content == b""


def test_get_location_context(
    db, created_product, created_location, created_category, created_measurement
):
    created_product.category = created_category
    created_product.save()
    item = Item.objects.create(
        name=created_product,
        location=created_location,
        measurement=created_measurement,
    )
    response = get_location_context(created_location.id)
    qs = response["rows"][0]["items"]
    response["rows"][0]["items"] = [item for item in qs]
    assert response == {
        "location": created_location,
        "location_id": created_location.id,
        "rows": [{"category": created_category, "items": [item]}],
    }


def test_get_index_context(db, created_product, created_location, created_measurement):
    Item.objects.create(
        name=created_product,
        location=created_location,
        measurement=created_measurement,
    )
    response = get_index_context()
    assert response == {
        "rows": [
            {
                "items_count": 1,
                "items_expired": 0,
                "items_expiring_soon": 0,
                "location": created_location,
            }
        ]
    }


def test_index(db):
    request = MagicMock()
    response = index(request)
    assert response.status_code == 200
    assert "<title>Home Inventory</title>" in str(response.content)


def test_location_detail(db, created_location):
    request = MagicMock()
    response = location_detail(request, created_location.id)
    assert response.status_code == 200
    assert f"<title>{created_location.name.title()}</title>" in str(response.content)


def test_add_location_post(db):
    request = MagicMock(method="POST")
    response = add_location(request)
    assert response.status_code == 200
    assert "<title>Home Inventory</title>" in str(response.content)


def test_add_location_form(db):
    request = MagicMock()
    response = add_location(request)
    assert response.status_code == 200
    assert "<title>Add Location</title>" in str(response.content)


def test_add_item_post(
    db, created_location, created_category, created_product, created_measurement
):
    data = {
        "name": created_product,
        "category": created_category,
        "location": created_location,
        "quantity": 3,
        "measurement": created_measurement,
    }
    request = MagicMock(method="POST", POST=data)
    response = add_item(request, created_location.id)
    assert response.status_code == 200
    assert f"<title>{created_location.name.title()}</title>" in str(response.content)


def test_add_item_form(db, created_location):
    request = MagicMock()
    response = add_item(request, created_location.id)
    assert response.status_code == 200
    assert "<title>Add Item</title>" in str(response.content)


def test_edit_item_post(
    db, created_location, created_category, created_product, created_measurement
):
    item = Item.objects.create(
        name=created_product,
        location=created_location,
        measurement=created_measurement,
    )
    data = {
        "name": created_product,
        "category": created_category,
        "location": created_location,
        "quantity": 3,
        "measurement": created_measurement,
    }
    request = MagicMock(method="POST", POST=data)
    response = edit_item(request, item.id)
    assert response.status_code == 200
    assert f"<title>{created_location.name.title()}</title>" in str(response.content)


def test_edit_item_form(db, created_location, created_product, created_measurement):
    item = Item.objects.create(
        name=created_product,
        location=created_location,
        measurement=created_measurement,
    )
    request = MagicMock()
    response = edit_item(request, item.id)
    assert response.status_code == 200
    assert "<title>Edit Item</title>" in str(response.content)


def test_delete_item_not_post():
    request = MagicMock()
    assert delete_item(request, 1) is None


def test_delete_item(db, created_location, created_product, created_measurement):
    item = Item.objects.create(
        name=created_product,
        location=created_location,
        measurement=created_measurement,
    )
    request = MagicMock(method="POST")
    response = delete_item(request, item.id)
    assert response.status_code == 200
    assert f"<title>{created_location.name.title()}</title>" in str(response.content)

    # check the item is really deleted
    with pytest.raises(Item.DoesNotExist):
        Item.objects.get(pk=item.id)
