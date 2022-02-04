from views import IndexPageView, navigate_to


def test_index(home_inventory_ui):
    index_view = navigate_to(home_inventory_ui, "IndexPage")
    index_view.wait_displayed()


def test_add_location(home_inventory_ui):
    test_location = "very exciting location"
    add_location_view = navigate_to(home_inventory_ui, "AddLocationPage")
    add_location_view.wait_displayed()

    # add testing location and check redirect back to the index page
    add_location_view.add_location(test_location)
    index_view = home_inventory_ui.create_view(IndexPageView)
    index_view.wait_displayed()

    # assert the location is added
    assert test_location in index_view.get_all_locations()
