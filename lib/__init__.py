
import sys
import os
import os.path

__directory__ = os.path.dirname(__file__)

sys.path.insert(0, __directory__)

# check for libusb1
_cwd = os.getcwd()
try:
    # make sure ctypes sees libusb-1.0.dll
    os.chdir(__directory__)

    try:
        import libusb1
        import usb1
    except import:
        from . import libusb1
        from . import usb1

finally:
    os.chdir(_cwd)
