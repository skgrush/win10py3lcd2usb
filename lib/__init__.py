
import sys
import os
import os.path

__directory__ = os.path.dirname(__file__)

sys.path.insert(0, __directory__)

# make sure ctypes sees libusb-1.0.dll
_cwd = os.getcwd()
try:
    os.chdir(__directory__)
    from . import libusb1
    from . import usb1
finally:
    os.chdir(_cwd)
