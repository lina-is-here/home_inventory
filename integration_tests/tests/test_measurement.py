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


def test_default_measurement_select():
    """
    The default measurement is selected but can be changed to another
    """
    pass


def test_default_measurement_only_one():
    """
    Only one measurement can be default, adding another violates DB constraint
    """
    pass
