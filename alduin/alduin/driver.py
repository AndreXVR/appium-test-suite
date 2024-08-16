from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


class Driver(WebDriver):
    @staticmethod
    def create(appium_server_url: str, capabilities: dict):
        return Driver(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def element(self, **kwargs):
        for key, value in kwargs.items():
            return self.find_element(by=AppiumBy.XPATH, value=f'//*[@{key}="{value}"]')
