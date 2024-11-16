import logging


def device_logger(name: str, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    consoleHandler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    return logger
