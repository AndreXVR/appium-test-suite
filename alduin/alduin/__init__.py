import os
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService, AppiumServiceError

from . import appium_config
from .driver import Driver

appium = AppiumService()


def device(name: str = None):
    print("here")
    os.system('appium')
    os.system('adb start-server')
    print("done")
    return Driver(name)
