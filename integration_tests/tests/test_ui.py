import requests
from selenium import webdriver
from wait_for import wait_for


def test_index():
    driver = "http://selenium-container:4444"
    test_page = "https://hi-nginx"

    def selenium_driver_is_available():
        r = requests.get(driver)
        return r.status_code == 200

    # check that selenium container is up and running
    wait_for(selenium_driver_is_available, delay=1, timeout=120, handle_exception=True)

    selenium_driver = webdriver.Remote(
        command_executor=f"{driver}/wd/hub",
        desired_capabilities={
            "platform": "LINUX",
            "browserName": "chrome",
            "unexpectedAlertBehaviour": "ignore",
            "acceptInsecureCerts": True,
            "ensureCleanSession": True,
        },
    )

    selenium_driver.get(test_page)
    selenium_driver.close()
