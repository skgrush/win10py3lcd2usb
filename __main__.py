#!/usr/bin/env python3
"""Main script for win10py3lcd2usb."""

import sys
import os
import os.path
import logging

__DIR__ = os.path.dirname(os.path.abspath(__file__))

try:
    import win10py3lcd2usb
    win10py3lcd2usb.init()
except ImportError:
    if 'win10py3lcd2usb' in sys.argv:
        import logging.config
        logging.config.fileConfig(os.path.join(__DIR__, "setup.cfg"))
        m = "You called me wrong; should've used `py -m win10py3lcd2usb`"
        print(m)
        logging.getLogger().critical(m)
    else:
        _cwd = os.getcwd()
        try:
            os.chdir(os.path.join(__DIR__, '..'))
            import win10py3lcd2usb
            win10py3lcd2usb.init()
        finally:
            os.chdir(_cwd)
    raise

# Pseudo-local imports
import lcd2usb  # noqa

# Local imports
from screens import ohw  # noqa

logger = logging.getLogger()


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
