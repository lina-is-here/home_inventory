import datetime

import pytest

from views import navigate_to


@pytest.fixture(scope="module")
def created_items(home_inventory_ui, postgres_connection):
    items = [
        {
            "name": "Canned Corn 1kg",
            "category": "Canned",
            "measurement": "pieces",
            "expiry_date": datetime.date.today().strftime("%m.%d.%Y"),
        },
        {
            "name": "Big Apple Juice 10L",
            "category": "Drinks",
            "measurement": "pieces",
            "expiry_date": datetime.date.today().strftime("%m.%d.%Y"),
        },
        {
            "name": "Big Box of Milk 5L",
            "category": "Drinks",
            "measurement": "pieces",
            "expiry_date": datetime.date.today().strftime("%m.%d.%Y"),
        },
    ]
    for item in items:
        location_view = navigate_to(home_inventory_ui, "FirstLocationPage")
        item_form = location_view.add_item()
        item_form.fill(item)
        item_form.save()

    yield

    # clear all the created stuff
    db_connection, db_cursor = postgres_connection
    db_cursor.execute("DELETE FROM inventory_category")
    db_cursor.execute("DELETE FROM inventory_product")
    db_cursor.execute("DELETE FROM inventory_item")
    db_connection.commit()


def test_category_is_displayed(home_inventory_ui, created_items):
    """
    Items are displayed per category
    """
    location_view = navigate_to(home_inventory_ui, "FirstLocationPage")
    pass


def test_quantity_is_displayed():
    """
    Quantity is displayed for each item
    """
    pass


def test_measurement_is_displayed():
    """
    Measurement is displayed for each item
    """
    pass


def test_expiry_date_is_displayed():
    """
    Expiry date is displayed for each item
    """
    pass


def test_expired_item():
    """
    Expired item is highlighted with red
    """
    pass


def test_expiring_soon_item():
    """
    Expiring soon item is highlighted with yellow
    """
    pass


def test_search_in_page():
    """
    Search on page works and filters out the results.
    * The results are case insensitive
    * The results are accent insensitive
    * The results are Cyrillic friendly, e.g. 'дом' should find 'dom'
    """
    pass
