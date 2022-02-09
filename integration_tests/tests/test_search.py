from views import navigate_to


def test_search_link(home_inventory_ui):
    index_view = navigate_to(home_inventory_ui, "IndexPage")
    assert "Search" in index_view.navbar.read()
