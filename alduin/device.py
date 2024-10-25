import re
import time

from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy

from alduin.appium_config import appium_server_url, capabilities
from alduin.constants import attributes_dict
from alduin.exceptions import ItemNotFoundException
from alduin.item import Item


class Device:
    def __init__(self, name: str):
        if name:
            capabilities["deviceName"] = name
        options = UiAutomator2Options().load_capabilities(capabilities)
        self._driver = WebDriver(appium_server_url, options=options)

    def back(self):
        self._driver.press_keycode(4)

    @property
    def height(self):
        return self._driver.get_window_size().get("height")

    @property
    def width(self):
        return self._driver.get_window_size().get("width")

    def find_item(self, timeout=0, **attributes_kwargs):
        elements = self._item_finder(attributes_kwargs, timeout)
        if len(elements) > 1:
            # TODO: Add logger with warning
            print("Warn about finding more than one item")
        return Item(elements[0])

    def find_items(self, timeout=0, **attributes_kwargs):
        elements = self._item_finder(attributes_kwargs, timeout)
        return [Item(element) for element in elements]

    def home(self):
        self._driver.press_keycode(3)

    def lock(self):
        self._driver.lock()

    def press_keycode(self, keycode: int):
        self._driver.press_keycode(keycode)

    def recents(self):
        self._driver.press_keycode(187)

    def shell(self, command: str):
        if command.strip():
            tokens = [token.strip() for token in command.split(" ")]
            cmd = tokens[0]
            if len(tokens) > 1:
                args = tokens[1:]
            return self._driver.execute_script("mobile: shell", {"command": cmd, "args": args})
        raise TypeError("Command cannot be empty")

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 0):
        self._driver.swipe(start_x, start_y, end_x, end_y, duration=duration)

    def swipe_item(
        self,
        max_swipes: int = 5,
        scroll_item: Item = None,
        duration: int = 600,
        direction: str = "up",
        **attributes_kwargs,
    ):
        elements = self._swipe_item_find(attributes_kwargs, max_swipes, scroll_item, duration, direction)
        return [Item(element) for element in elements]

    def unlock(self):
        self._driver.unlock()

    def volume_up(self):
        self._driver.press_keycode(24)

    def volume_down(self):
        self._driver.press_keycode(25)

    def _build_xpath(self, attributes_kwargs):
        self._validate_kwargs(attributes_kwargs)
        xpath = ""
        for key, value in attributes_kwargs.items():
            if isinstance(value, str):
                value = re.compile(rf"^{value}$")
            xpath += f" and matches(@{attributes_dict[key]}, '{value.pattern}')"
        xpath = f"[{xpath[5:]}]"
        xpath = "//*" + xpath if attributes_kwargs else "//*"
        return xpath

    def _validate_kwargs(self, attributes_kwargs):
        attrib_set = set(attributes_dict.keys())
        difference = set(attributes_kwargs.keys()).difference(attrib_set)
        if difference:
            raise TypeError(f"Unexpected keyword arguments {str(difference)}")
        for key, value in attributes_kwargs.items():
            if not isinstance(value, str) and not isinstance(value, re.Pattern):
                raise TypeError(f'Argument "{key}" is not a string or regular expression')

    def _item_finder(self, attributes_kwargs, timeout=0):
        start = time.perf_counter()
        xpath = self._build_xpath(attributes_kwargs)
        timed_out = False
        elements = []
        while not timed_out and not elements:
            timed_out = time.perf_counter() >= start + timeout
            elements = self._driver.find_elements(by=AppiumBy.XPATH, value=xpath)
        if not elements:
            raise ItemNotFoundException(f"Could not find any items with {attributes_kwargs}")
        return elements

    def _swipe_coords(self, item, direction: str = "up"):
        bounds = item.bounds if item else dict(start_x=0, start_y=0, end_x=self.width, end_y=self.height)
        center = dict(x=(bounds["start_x"] + bounds["end_x"]) / 2, y=(bounds["start_y"] + bounds["end_y"]) / 2)
        coords = dict(start_x=center["x"], start_y=center["y"], end_x=center["x"], end_y=center["y"])
        match direction:
            case "up":
                coords["end_y"] = bounds["start_y"]
            case "down":
                coords["end_y"] = bounds["end_y"]
            case "left":
                coords["end_y"] = bounds["start_x"]
            case "right":
                coords["end_y"] = bounds["end_x"]
        return coords

    def _swipe_item_find(self, attributes_kwargs, max_swipes: int, scroll_item: Item, duration: int, direction: str):
        coords = self._swipe_coords(scroll_item, direction)
        elements = []
        swipes = 0
        while not elements and swipes <= max_swipes:
            try:
                elements = self._item_finder(attributes_kwargs)
            except ItemNotFoundException:
                swipes += 1
                self._driver.swipe(**coords, duration=duration)
        if not elements:
            raise ItemNotFoundException(f"Could not find any items with {attributes_kwargs}")
        return elements
