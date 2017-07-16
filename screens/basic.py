"""Basic one-time screen."""

import datetime

import lcd2usb


def basic(lcd: lcd2usb.LCD):
    """Output basic LCD information and datetime."""
    bus, dev = lcd.info(False)
    version = lcd.version
    now = datetime.datetime.now()
    lcd.clear()
    lcd.fill('LCD Version: {0}.{1}'.format(*version), 0)
    lcd.fill('Bus: {0:x}, Dev: {1:x}'.format(bus, dev), 1)
    lcd.fill(str(now), 2)
    lcd.fill_center('win10py3lcd2usb', 3)
