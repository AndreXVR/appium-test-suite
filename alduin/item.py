from alduin.constants import attributes


class Item:
    @staticmethod
    def _format_value(value: str):
        if value != 'true' and value != 'false':
            return value
        return value == 'true'

    def __init__(self, element):
        self._element = element
        # TODO: make items dinamic, by using an element to get itself
        for attr_key, attr_value in attributes.items():
            value = element.get_attribute(attr_value)
            setattr(self, attr_key, Item._format_value(value))
