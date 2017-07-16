#!/usr/bin/env python3
"""Just a script for testing lcd stuff."""

import os
import logging

# Pseudo-local imports
import lcd2usb

# Local imports
import _logging  # noqa
import atexitLCD  # noqa
from screens import ohw


logger = logging.getLogger("testing")


if not os.isatty(0):
    fl = open("print.log", "a+")
    os.stdout = fl


if __name__ == '__main__':

    # pylint: disable=broad-except
    try:
        ohw.screen(lcd2usb.LCD(), 0.5)
    except KeyboardInterrupt:
        logger.info("Exiting due to KeyboardInterrupt")
    except Exception:
        logger.critical("Exiting due to fatal exception.", exc_info=True)
        import traceback
        traceback.print_exc()
