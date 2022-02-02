from wait_for import wait_for

from views import navigate_to


def test_index(home_inventory_ui):
    index_view = navigate_to(home_inventory_ui, "IndexPage")
    wait_for(
        lambda: index_view.is_displayed,
        timeout=60,
        message="Wait for index view",
        delay=5,
    )
