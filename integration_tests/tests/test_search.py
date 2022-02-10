from views import navigate_to


def test_search_link(home_inventory_ui):
    """
    Search is there in the navbar
    """
    index_view = navigate_to(home_inventory_ui, "IndexPage")
    assert "Search" in index_view.navbar.read()


def test_search_by_name():
    """
    Search works by name
    * The results are case insensitive
    * The results are accent insensitive
    * The results are Cyrillic friendly, e.g. 'дом' should find 'dom'
    """
    pass


def test_search_by_barcode():
    """
    Search works by barcode and returns all products in all locations
    """
    pass


def test_search_by_name_or_barcode():
    """
    Search only works when either name or barcode is provided.
    Search doesn't work when both are provided.
    Search doesn't work when none are provided.
    """
    pass
