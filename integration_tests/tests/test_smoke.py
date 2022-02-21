"""
Test the very basic functionality of the app.
"""
import datetime

from views import IndexPageView, navigate_to

# from base import add_measurement


def test_index(home_inventory_ui):
    """
    The index page is displayed.
    """
    index_view = navigate_to(home_inventory_ui, "IndexPage")
    index_view.wait_displayed()


def test_add_location(home_inventory_ui):
    """
    A location can be added and then it is displayed on the index page.
    """
    test_location = "very exciting location"
    add_location_view = navigate_to(home_inventory_ui, "AddLocationPage")

    # add testing location and check redirect back to the index page
    index_view = add_location_view.add_location(test_location)

    # assert the location is added
    assert test_location in index_view.get_all_locations()


def test_item_measurements(home_inventory_ui, add_measurement):
    """
    The measurement is displayed in the dropdown after it is added to the database.
    """
    new_measurement = "tablets"
    add_measurement(new_measurement)

    location_view = navigate_to(home_inventory_ui, "FirstLocationPage")
    item_form = location_view.add_item()

    # assert new measurement is visible and selectable in AddItem form
    all_measurements = [option.text for option in item_form.measurement.all_options]
    assert new_measurement in all_measurements
    item_form.measurement.select_by_visible_text(new_measurement)
    assert item_form.measurement.first_selected_option == new_measurement


def test_add_item(home_inventory_ui):
    """
    An item can be added and is displayed in the location view.
    """
    item_name = "Kofola 250ml"
    item = {
        "name": item_name,
        "category": "Drinks",
        "measurement": "pieces",
        "expiry_date": datetime.date.today().strftime("%m.%d.%Y"),
    }
    location_view = navigate_to(home_inventory_ui, "FirstLocationPage")
    item_form = location_view.add_item()
    item_form.fill(item)
    location_view = item_form.save()

    # assert the item is visible on location page
    assert item_name in location_view.all_items()
