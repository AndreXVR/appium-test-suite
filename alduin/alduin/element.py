from appium.webdriver.webelement import WebElement



class Element(WebElement):
    def __init__(self, element):
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
