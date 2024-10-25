import os

from appium import webdriver
from appium.options.android import UiAutomator2Options

appium_server_url = 'http://localhost:4723'

appium_server_url = 'http://localhost:4723'

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2'
)

os.system('appium')
os.system('adb start-server')

print(type(webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))))
