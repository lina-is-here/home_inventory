import psycopg2
import pytest
from views import navigate_to


def test_default_measurement(home_inventory_ui, add_measurement):
    """
    The default measurement is displayed on AddItem form
    """
    default_measurement = "kusochki"
    add_measurement(default_measurement, True)
    # TODO: this is ugly
    add_location_view = navigate_to(home_inventory_ui, "AddLocationPage")
    index_view = add_location_view.add_location("some location")
    location_view = index_view.navigate_first_location()
    item_form = location_view.add_item()
    assert item_form.measurement.first_selected_option == default_measurement


def test_no_default_measurement(home_inventory_ui, postgres_connection):
    """
    If there's no default measurement, '---------' is displayed
    """
    db_connection, db_cursor = postgres_connection
    db_cursor.execute("SELECT id FROM inventory_measurement WHERE is_default=true;")
    assert db_cursor.fetchone() is None  # no default measurement in the database
    db_connection.commit()
    index_view = navigate_to(home_inventory_ui, "IndexPage")
    location_view = index_view.navigate_first_location()
    item_form = location_view.add_item()
    assert item_form.measurement.first_selected_option == "---------"


def test_default_measurement_select(home_inventory_ui, add_measurement):
    """
    The default measurement is selected but can be changed to another
    """
    default_measurement = "paketiki"
    other_measurement = "sumki"
    add_measurement(default_measurement, True)
    add_measurement(other_measurement)
    index_view = navigate_to(home_inventory_ui, "IndexPage")
    location_view = index_view.navigate_first_location()
    item_form = location_view.add_item()
    assert item_form.measurement.first_selected_option == default_measurement
    item_form.measurement.select_by_visible_text(other_measurement)
    assert item_form.measurement.first_selected_option == other_measurement


def test_default_measurement_only_one(add_measurement):
    """
    Only one measurement can be default, adding another violates DB constraint
    """
    default_measurement = "shtuki"
    other_measurement = "shtuchki"
    add_measurement(default_measurement, True)
    with pytest.raises(psycopg2.Error):
        add_measurement(other_measurement, True)
