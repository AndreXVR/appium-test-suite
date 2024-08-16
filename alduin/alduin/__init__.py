from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from appium.options.android import UiAutomator2Options

from . import appium_config
from .driver import Driver

def use():
    appium_service = AppiumService()
    print(appium_service)
    if not appium_service.is_running:
        appium_service.start()
    return Driver.create(appium_server_url=appium_config.appium_server_url, capabilities=appium_config.capabilities)
