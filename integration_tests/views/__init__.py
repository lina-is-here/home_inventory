from navmazing import Navigate, NavigateToSibling
from wait_for import wait_for
from widgetastic.widget import View, Text, TextInput

from base.browser import HI_UI, HINavigateStep
from base.widgetastic_widgets import Button


class BasePageView(View):
    title = Text(locator=".//title")
    # TODO: navbar and footer are not Text widgets
    navbar = Text(locator=".//nav")
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

    def get_location(self):
        """Get the first location"""
        return self.location.read()

    def get_all_locations(self):
        """Get all created locations names"""
        return [
            el.accessible_name for el in self.browser.elements(self.location.locator)
        ]


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


# ------------------Navigation---------------------------#
navigator = Navigate()
navigate_to = navigator.navigate


@navigator.register(HI_UI)
class IndexPage(HINavigateStep):
    VIEW = IndexPageView

    def am_i_here(self):
        return self.view.is_displayed

    def step(self):
        self.obj.create_view(BasePageView)


@navigator.register(HI_UI)
class AddLocationPage(HINavigateStep):
    VIEW = AddLocationView
    prerequisite = NavigateToSibling("IndexPage")

    def am_i_here(self):
        return self.view.is_displayed

    def step(self):
        self.prerequisite_view.add_location()
        wait_for(
            lambda: self.view.is_displayed,
            timeout=60,
            message=f"Wait for {self.view}",
            delay=1,
        )
