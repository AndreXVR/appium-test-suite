from logging import INFO

from alduin.device import Device


def init(serial: str = None, host="127.0.0.1", appium_port=4723, adb_port=5037, log_level=INFO):
    return Device(serial, host, appium_port, adb_port, log_level)
