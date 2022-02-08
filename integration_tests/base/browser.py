import os

import pytest
import requests
from cached_property import cached_property
from navmazing import NavigateStep, NavigationTriesExceeded
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from wait_for import wait_for
from widgetastic.browser import Browser

DRIVER = os.environ.get("SELENIUM_DRIVER", "http://selenium-container:4444")
TEST_PAGE = os.environ.get("TEST_HOST", "https://hi-nginx")


class HI_UI(Browser):
    def create_view(self, view_class):
        return view_class(self)

    def go_home(self):
        return self.selenium.get(TEST_PAGE)


class HINavigateStep(NavigateStep):
    VIEW = None

    @cached_property
    def view(self):
        if self.VIEW is None:
            raise AttributeError(
                "{} does not have VIEW specified".format(type(self).__name__)
            )
        return self.create_view(self.VIEW)

    def create_view(self, *args, **kwargs):
        return self.obj.create_view(*args, **kwargs)

    def am_i_here(self):
        try:
            return self.view.is_displayed
        except (AttributeError, NoSuchElementException):
            return False

    def go(self, _tries=0, *args, **kwargs):
        nav_args = {"use_resetter": True, "wait_for_view": False}
        if _tries > 2:
            raise NavigationTriesExceeded(f"{self._name}")

        _tries += 1
        for arg in nav_args:
            if arg in kwargs:
                nav_args[arg] = kwargs.pop(arg)

        here = False
        try:
            # Testing out not wrapping the am_i_here call in the pre nav prep
            here = self.am_i_here()
        except Exception:
            pass

        if not here:
            self.prerequisite_view = self.prerequisite()
            self.step()

        view = self.view if self.VIEW is not None else None
        if (
            view
            and nav_args["wait_for_view"]
            and not os.environ.get("DISABLE_NAVIGATE_ASSERT", False)
        ):
            wait_for(
                lambda: view.is_displayed,
                num_sec=10,
                message=f"Waiting for view [{view.__class__.__name__}] to display",
            )
        return view


@pytest.fixture(scope="session")
def home_inventory_ui():
    def selenium_driver_is_available():
        r = requests.get(DRIVER)
        return r.status_code == 200

    # check that selenium container is up and running
    wait_for(selenium_driver_is_available, delay=1, timeout=120, handle_exception=True)

    # set desired capabilities to the driver
    options = Options()
    capabilities = {
        "platformName": "LINUX",
        "unexpectedAlertBehaviour": "ignore",
        "acceptInsecureCerts": True,
        "ensureCleanSession": True,
    }
    for name, value in capabilities.items():
        options.set_capability(name, value)

    selenium_driver = webdriver.Remote(
        command_executor=f"{DRIVER}/wd/hub",
        options=options,
    )

    wt_browser = HI_UI(selenium_driver)
    wt_browser.selenium.get(TEST_PAGE)
    yield wt_browser

    wt_browser.selenium.close()
    wt_browser.selenium.quit()
