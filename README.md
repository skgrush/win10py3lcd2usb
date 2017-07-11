




## Dependencies
### Python 3
Developed for Python 3.\*, tested with Python 3.6.

### lcd2usb
**Currently included in [lib/](lib/)**

Requires the [`lcd2usb`][xyb-lcd2usb] module by [xyb][xyb-github]. Beware that xyb's module is not Python 3 compatible, but the one in [lib/](lib/) is.

#### libusb, python-libusb1
**Currently included in [lib/](lib/)**

The `lcd2usb` module requires [python-libusb1][vpelletier-libusb1], installable via
```shell
$ pip install libusb1
```
The binary [libusb-1.0](lib/libusb-1.0.dll) may be required (included in [lib/](lib/)).

Additionally it (should) require a driver to communicate with the LCD, which is installable with a program called [Zadig][zadig].


## Recommended Packages
### wmi, pywin32

Modules in [wmi_interfaces/](wmi_interfaces/) require the [`wmi`][timgolden-wmi] module, which requires the [`pywin32`][sf-pywin32] extensions. These are both installable via
```shell
$ pip install wmi pypiwin32
```
Notice that it's "py**pi**win32" on pypi.



[xyb-github]: https://github.com/xyb
[xyb-lcd2usb]: https://github.com/xyb/lcd2usb
[vpelletier-libusb1]: https://github.com/vpelletier/python-libusb1
[timgolden-wmi]: http://timgolden.me.uk/python/wmi/index.html
[sf-pywin32]: https://sourceforge.net/projects/pywin32/
[zadig]: http://zadig.akeo.ie/
