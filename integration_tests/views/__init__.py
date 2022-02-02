from navmazing import Navigate
from widgetastic.widget import View, Text

from base.browser import HI_UI, HINavigateStep


class BasePageView(View):
    title = Text(locator=".//title")

    @property
    def is_displayed(self):
        return self.title.is_displayed


class IndexPageView(BasePageView):
    @property
    def is_displayed(self):
        return self.title.text == "Home Inventory"


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
