from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from alduin.constants import attributes
from alduin.item import Item


class Device:
    appium_server_url = 'http://localhost:4723'
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        newCommandTimeout=0
    )

    def __init__(self, device_name: str = None):
        if device_name:
            self.capabilities['deviceName'] = device_name
        options = UiAutomator2Options().load_capabilities(self.capabilities)
        self.driver = webdriver.Remote(self.appium_server_url, options=options)

    def _validate_kwargs(self, kwargs):
        attrib_set = set(attributes.keys())
        difference = set(kwargs.keys()).difference(attrib_set)
        if difference:
            raise TypeError(f'Unexpected keyword arguments {str(difference)}')

    def item(self, **kwargs):
        self._validate_kwargs(kwargs)
        xpath = ''
        for key, value in kwargs.items():
            xpath += f' and @{attributes[key]}=\'{value}\''
        xpath = f'[{xpath[5:]}]'
        xpath = '//*'+xpath if kwargs else '//*'
        print(xpath)
        return Item(self.driver.find_element(by=AppiumBy.XPATH, value=xpath))
