from navmazing import Navigate, NavigateToSibling
from selenium.common.exceptions import NoSuchElementException
from wait_for import wait_for
from widgetastic.widget import View, Text, TextInput, Select, Table, TableRow

from base.browser import HI_UI, HINavigateStep
from base.widgetastic_widgets import Button, Select2, Navbar


class BasePageView(View):
    title = Text(locator=".//title")
    # TODO: footer is not Text widget
    navbar = Navbar(locator=".//nav")
    footer = Text(locator=".//footer")

    @property
    def is_displayed(self):
        return self.title.is_displayed


class IndexPageView(BasePageView):
    add_location_button = Button(locator=".//a[@id='add-location-button']")
    location = Button(locator=".//a[contains(@class, 'location')]")

    @property
    def is_displayed(self):
        return (
            self.title.text == "Home Inventory"
            and self.add_location_button.is_displayed
        )

    def add_location(self):
        """Click Add Location button"""
        self.add_location_button.click()

    def get_first_location(self):
        """Get the first location"""
        return self.location.read()

    def get_all_locations(self):
        """Get all created locations names"""
        return [
            el.accessible_name for el in self.browser.elements(self.location.locator)
        ]

    def navigate_first_location(self):
        """Navigate to the first location in the list"""
        self.location.wait_displayed()
        self.location.click()
        return self.browser.create_view(LocationView)


class AddLocationView(BasePageView):
    breadcrumb = Text(locator=".//ol[@class='breadcrumb']")
    location_input = TextInput(locator=".//input[@id='id_name']")
    submit_button = Button(locator=".//input[@id='submit-id-submit']")

    @property
    def is_displayed(self):
        return self.breadcrumb.is_displayed and self.location_input.is_displayed

    def add_location(self, location_name):
        self.location_input.fill(location_name)
        self.submit_button.click()
        return self.browser.create_view(IndexPageView)


class LocationView(BasePageView):
    breadcrumb = Text(locator=".//ol[@class='breadcrumb']")
    add_button = Button(locator=".//a[@id='add-item-button']")
    items = Table(locator=".//table[@id='items-table']")

    @property
    def is_displayed(self):
        return self.breadcrumb.is_displayed and self.add_button.is_displayed

    def add_item(self):
        self.add_button.click()
        return self.browser.create_view(ItemFormView)

    def all_items(self):
        items = []
        for row in self.items:
            try:
                items.append(row[0].text)
            except NoSuchElementException:
                continue
        return items


class ItemFormView(BasePageView):
    breadcrumb = Text(locator=".//ol[@class='breadcrumb']")
    save_button = Button(locator=".//input[@id='submit-id-submit']")
    name = Select2(locator=".//span[@id='select2-id_name-container']")
    barcode = TextInput(id="id_barcode")
    category = Select2(locator=".//span[@id='select2-id_category-container']")
    quantity = TextInput(id="id_quantity")  # this is number input in fact
    measurement = Select(id="id_measurement")
    expiry_date = TextInput(id="id_expiry_date")  # this is date input in fact
    location = Select(id="id_location")

    @property
    def is_displayed(self):
        return self.breadcrumb.is_displayed and self.save_button.is_displayed

    def save(self):
        self.save_button.click()
        return self.browser.create_view(LocationView)


class EditItemFormView(ItemFormView):
    """Almost the same but has 'Remove' button"""

    remove_button = Button(locator=".//input[@value='remove']")

    @property
    def is_displayed(self):
        return (
            self.breadcrumb.is_displayed
            and self.save_button.is_displayed
            and self.remove_button.is_displayed
        )

    def remove(self):
        self.remove_button.click()
        return self.browser.create_view(LocationView)


class SearchView(BasePageView):
    breadcrumb = Text(locator=".//ol[@class='breadcrumb']")
    product_name = TextInput(id="id_name")
    product_barcode = TextInput(id="id_barcode")
    search_button = Button(locator=".//input[@id='submit-id-submit']")

    @property
    def is_displayed(self):
        return (
            self.breadcrumb.is_displayed
            and self.product_name.is_displayed
            and self.product_barcode.is_displayed
            and self.search_button.is_displayed
        )

    def search(self):
        self.search_button.click()


# ------------------Navigation---------------------------#
navigator = Navigate()
navigate_to = navigator.navigate


@navigator.register(HI_UI)
class IndexPage(HINavigateStep):
    VIEW = IndexPageView

    def am_i_here(self):
        return self.view.is_displayed

    def step(self):
        self.obj.go_home()
        self.obj.create_view(IndexPageView)


@navigator.register(HI_UI)
class AddLocationPage(HINavigateStep):
    VIEW = AddLocationView
    prerequisite = NavigateToSibling("IndexPage")

    def am_i_here(self):
        return self.view.is_displayed

    def step(self):
        self.prerequisite_view.add_location()


@navigator.register(HI_UI)
class FirstLocationPage(HINavigateStep):
    VIEW = LocationView
    prerequisite = NavigateToSibling("IndexPage")

    def am_i_here(self):
        return self.view.is_displayed

    def step(self):
        self.prerequisite_view.navigate_first_location()


@navigator.register(HI_UI)
class SearchViewPage(HINavigateStep):
    VIEW = SearchView

    def am_i_here(self):
        return self.view.is_displayed

    def step(self):
        # search is accessible from any page
        view = self.obj.create_view(BasePageView)
        # TODO: click on the Search link
