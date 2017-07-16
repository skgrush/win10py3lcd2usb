
import sys
import os
import os.path
import logging

__all__ = ('lcd2usb', 'usb1')

logger = logging.getLogger(__name__)

__directory__ = os.path.dirname(__file__)
sys.path.append(__directory__)

libusb_driver_dir = os.path.join(__directory__, 'usb1/drivers')

# check for libusb1
_cwd = os.getcwd()
try:
    # make sure ctypes sees libusb-1.0.dll
    os.chdir(libusb_driver_dir)

    from . import usb1
except OSError:
    logger.warning("Failed to load usb1")
    raise

finally:
    os.chdir(_cwd)

print(usb1)
