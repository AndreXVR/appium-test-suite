import re

from alduin.constants import attributes_dict


class Item:
    @property
    def coords(self):
        pattern = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")
        match = pattern.search(self._element.bounds)
        return dict(start_x=match.group(1), start_y=match.group(2), end_x=match.group(3), end_y=match.group(4))

    def tap(self):
        self._element.click()

    def __init__(self, element):
        self._element = element
        # TODO: make items dinamic, by using an element to get itself if stale
        for attr_key, attr_value in attributes_dict.items():
            value = element.get_attribute(attr_value)
            setattr(self, attr_key, Item._format_value(value))

    def __repr__(self):
        output = "Item("
        for key in attributes_dict.keys():
            output += f"{key}={getattr(self, key, None)}, "
        return output[:-2]+")"

    @staticmethod
    def _format_value(value: str):
        if value != "true" and value != "false":
            return value
        return value == "true"

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        attributes_to_compare = list(attributes_dict.keys())
        attributes_to_compare.remove("bounds")
        for key in attributes_to_compare:
            if getattr(self, key, None) != getattr(other, key, None):
                return False
        return True
