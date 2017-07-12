
import sys
import os
import os.path

__directory_ = os.path.dirname(__file__)

sys.path.insert(0, __directory_)

# check for libusb1
_cwd = os.getcwd()
try:
    # make sure ctypes sees libusb-1.0.dll
    os.chdir(__directory_)

    try:
        import libusb1
        import usb1
    except ImportError:
        from . import libusb1
        from . import usb1

finally:
    os.chdir(_cwd)
