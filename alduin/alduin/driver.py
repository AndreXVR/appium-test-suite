from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


class Driver(WebDriver):
    appium_server_url = 'http://localhost:4723'

    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2'
    )

    def __init__(self, device_name: str = None):
        if device_name:
            self.capabilities['deviceName'] = device_name
        options = UiAutomator2Options().load_capabilities(self.capabilities)
        print(self.appium_server_url)
        print(self.capabilities)
        return webdriver.Remote(self.appium_server_url, options=options)

    def element(self, **kwargs):
        for key, value in kwargs.items():
            return self.find_element(by=AppiumBy.XPATH, value=f'//*[@{key}="{value}"]')
