from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from urllib3.exceptions import NewConnectionError

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
        try:
            self.driver = webdriver.Remote(self.appium_server_url, options=options)
        except NewConnectionError as e:
            raise AssertionError('Make sure appium server is running.') from e

    def _validate_kwargs(self, kwargs):
        attrib_set = set(attributes.keys())
        difference = set(kwargs.keys()).difference(attrib_set)
        if difference:
            raise TypeError(f'Unexpected keyword arguments {str(difference)}')

    def item(self, **kwargs):
        self._validate_kwargs(kwargs)
        attribute = ''
        for key, value in kwargs.items():
            attribute += f' and @{key}=\'{value}\''
        attribute = f'[{attribute[5:]}]'
        filters = '//*'+attribute if kwargs else '//*'
        return Item(self.driver.find_element(by=AppiumBy.XPATH, value=filters))
