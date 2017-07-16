"""Import this to add an atexit listener that prints some info."""

from time import ctime as _ctime


def _get_lcd2usb():
    """Ideally import lcd2usb."""
    try:
        import lcd2usb
    except ImportError:
        try:
            from lib import lcd2usb
        except ImportError:
            try:
                from .lib import lcd2usb
            except ImportError:
                return None
    return lcd2usb


def _atexit_function():
    lcd2usb = _get_lcd2usb()
    if not lcd2usb:
        return

    try:
        lcd = lcd2usb.LCD()
    except lcd2usb.LCD2USBNotFound:
        return
    except Exception as exc:
        if type(exc).__name__ == 'USBErrorAccess':
            print("\nCan't clear screen: USB Access Error")
            return
        else:
            print("\nCan't clear screen:\n")
            raise

    ver = lcd.version

    lcd.clear()
    if ver == (-1, -1):
        lcd.fill_center("LCD2USB's fucked")
    else:
        lcd.fill_center("LCD2USB fw v{}.{}".format(*ver), 0)

    lcd.fill_center("win10py3lcd2usb exit", 2)
    lcd.fill(_ctime(), 3)

    lcd._flush()


import atexit as _atexit
_atexit.register(_atexit_function)
