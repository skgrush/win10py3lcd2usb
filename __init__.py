#!/usr/bin/env python3
"""win10py3lcd2usb __init__ file."""

import os
import os.path
import sys
import logging
import logging.config


__directory__ = os.path.dirname(__file__)


def _init_logging():
    logging.config.fileConfig(os.path.join(__directory__, "setup.cfg"))
    return logging.getLogger()


def _init_usb1(logger):
    """Initialize usb1 module using the driver in lib."""
    # check for libusb1
    _cwd = os.getcwd()
    try:
        # make sure ctypes sees lib/libusb-1.0.dll
        os.chdir(os.path.join(__directory__, 'lib/usb1/drivers'))
        try:
            import usb1
            logger.debug("Imported usb1 externally")
        except ImportError:

            from lib import usb1
            logger.debug("Imported usb1 from lib")

    finally:
        os.chdir(_cwd)

    return usb1


def _init_lcd(logger):
    """lcd2usb initial import to check that it's available.

    Is this necessary?
    """
    try:
        import lcd2usb  # noqa
        logger.info("Imported lcd2usb externally")
    except ImportError:
        logger.info("Importing lcd2usb from lib")
        from lib import lcd2usb  # noqa


def init():
    """Initialize the environment."""
    if __directory__ not in sys.path:
        sys.path.insert(0, __directory__)
    print("sys.path:", sys.path, "\n")

    logger = _init_logging()
    logger.debug("__init__.init() running")
    print(logger)

    _init_usb1(logger)
    _init_lcd(logger)

    import atexitLCD  # noqa
