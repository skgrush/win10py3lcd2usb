"""Characters defined for the HD44780 LCD controller.

Two handy tools for designing characters:
https://www.quinapalus.com/hd44780udg.html
https://omerk.github.io/lcdchargen/
"""

_fullblock = '\u2588'


class Char(bytes):
    """Character class.

    Characters are 8 rows of 5 bits.
    """

    __slots__ = ()

    def __new__(cls, rows):
        """Construct Char from an iterable or int.

        `rows` argument should be an iterator of pixel rows.
        """
        if isinstance(rows, int):
            rows = rows.to_bytes(8, 'big')
        elif isinstance(rows, str):
            rows = bytes(rows, 'ascii')
        else:
            rows = bytes(rows)

        assert isinstance(rows, bytes)

        if len(rows) > 8:
            rows = rows[-8:]
        else:
            rows = rows.rjust(8, b'\x00')

        assert len(rows) == 8

        return super().__new__(cls, rows)

    def __str__(self):
        """Printable character using unicode full blocks.

        If your platform or application doesn't like unicode characters, just
        change the module variable `__fullblock`.
        """
        return "\n".join("{:0>5b}".format(row) for row in self) \
               .replace('0', ' ').replace('1', _fullblock)

    def __int__(self):
        """Convert Char to integer."""
        return int.from_bytes(self, 'big')


BAR_8 = Char(0 * [0x00] + 8 * [0x1f])
BAR_7 = Char(1 * [0x00] + 7 * [0x1f])
BAR_6 = Char(2 * [0x00] + 6 * [0x1f])
BAR_5 = Char(3 * [0x00] + 5 * [0x1f])
BAR_4 = Char(4 * [0x00] + 4 * [0x1f])
BAR_3 = Char(5 * [0x00] + 3 * [0x1f])
BAR_2 = Char(6 * [0x00] + 2 * [0x1f])
BAR_1 = Char(7 * [0x00] + 1 * [0x1f])
BAR_0 = Char(8 * [0x00] + 0 * [0x1f])
