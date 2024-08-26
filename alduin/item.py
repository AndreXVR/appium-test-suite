from alduin.constants import attributes


class Item:
    def __init__(self, element):
        self._element = element
        for key, value in attributes.items():
            setattr(self, key, element.get_attribute(value))
