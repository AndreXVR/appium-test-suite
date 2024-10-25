from builtins import Exception


class ItemNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
