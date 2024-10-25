import re

from alduin.constants import attributes_dict


class Item:
    @property
    def bounds(self):
        pattern = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")
        match = pattern.search(self._element.bounds)
        return dict(start_x=match.group(1), start_y=match.group(2), end_x=match.group(3), end_y=match.group(4))

    def __init__(self, element):
        self._element = element
        # TODO: make items dinamic, by using an element to get itself if stale
        for attr_key, attr_value in attributes_dict.items():
            value = element.get_attribute(attr_value)
            setattr(self, attr_key, Item._format_value(value))

    @staticmethod
    def _format_value(value: str):
        if value != "true" and value != "false":
            return value
        return value == "true"
