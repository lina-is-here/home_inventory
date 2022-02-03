from navmazing import Navigate
from widgetastic.widget import View, Text

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

    @property
    def is_displayed(self):
        return (
            self.title.text == "Home Inventory"
            and self.add_location_button.is_displayed
        )

    def add_location(self, location_name):
        """Add location from index page"""
        self.add_location_button.click()
        # TODO: finish this method


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
