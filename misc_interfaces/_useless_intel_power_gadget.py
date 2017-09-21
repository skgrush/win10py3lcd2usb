"""Parser for Intel's CPU power gadget log.

Log Columns:
    System Time
    RDTSC
    Elapsed Time (sec)
    CPU Frequency_0(MHz)
    Processor Power_0(Watt)
    Cumulative Processor Energy_0(Joules)
    Cumulative Processor Energy_0(mWh)
    IA Power_0(Watt)
    Cumulative IA Energy_0(Joules)
    Cumulative IA Energy_0(mWh)
    Package Temperature_0(C)
    Package Hot_0
    Package Power Limit_0(Watt)

Sizes:
    Header:
        297 characters
    Line:
        116 characters
    Tail:
        Min: 350 characters
        mid: 375
        Max: 400 characters

    Empty:
        < 816



Last log line should always be < 530 characters from the end of the file.

"""

import io
import os
import sys
import pathlib
import re
from typing import Union

OFFSET_LOG_END = 550
READ_SIZE = 250

LAZY_LINE_RE = re.compile(r'((?:[\d:.]+, *)+(?:[\d:.]+))\n')
HEADER_RE = re.compile(r'(?P<label>[^,\n()]+)(?: ?\((?P<unit>[^,\n()]+)\))?')
SEP_RE = re.compile(r' *, *')

LABELS = (
    'System Time',
    'RDTSC',
    'Elapsed Time',
    'CPU Frequency',
    'Processor Power',
    'Cumulative Processor Energy',  # J|mWh ?
    'IA Power',
    'Cumulative IA Energy',  # J|mWh ?
    'Package Temperature',
    'Package Hot',
    'Package Power Limit'
)


def _guess_log_path(hint: Union[str, pathlib.Path]=None) -> pathlib.Path:
    """Guesses the log path, with optional hint.

    If hint is a file, return it.
    If hint is a directory, search it for 'PwrData*.csv'.
    If 'HOME' or 'USERPROFILE' environment variable are set, search it for
        'PwrData*.csv'.
    Else None.
    """
    path = pathlib.Path(hint) if hint else None
    home = os.environ.get('HOME', os.environ.get('USERPROFILE'))

    if path and path.exists():
        if path.is_file():
            return path
        elif not path.is_dir():
            return None
    elif home:
        path = pathlib.Path(home) / 'Documents'
    else:
        return None

    results = list(path.glob('PwrData*.csv'))

    if results:
        return sorted(results)[-1]


def read_logfile(logfile: io.TextIOBase) -> str:
    """Read the last chunk of logfile."""
    endpos = logfile.seek(0, 2)
    logfile.seek(max(0, endpos - OFFSET_LOG_END))
    return logfile.read(READ_SIZE)


def parse_log_headers(headers: str) -> (('label', 'unit'),):
    """Parse the headers line of the log file.

    Returns:
        (2-tuple tuple) mapping of labels to units.

    """
    return tuple((label, (unit or None))
                 for label, unit in HEADER_RE.findall(headers))


def parse_log_line(line: str) -> ('value', ):
    """Parse one line of the log file.

    Returns:
        (tuple) the values as strings.

    """
    return tuple(SEP_RE.split(line))


def get_values(logfile: io.TextIOBase or 'path') -> tuple:
    """Read latest values from logfile and return them as a tuple."""
    contents = None
    if isinstance(logfile, (str, pathlib.PurePath)):
        with open(logfile, 'r') as open_logfile:
            contents = read_logfile(open_logfile)
    else:
        contents = read_logfile(logfile)

    lines = LAZY_LINE_RE.findall(contents)

    return parse_log_line(lines[-1]) if lines else ()


def main():
    """Run the a demo script."""
    from time import perf_counter

    hint = None
    if len(sys.argv) > 1:
        hint = sys.argv[1]
    logpath = _guess_log_path(hint)

    if logpath:
        print("Logpath:", logpath)
        print("Getting values:")

        with open(logpath, 'r') as ofl:
            headers = parse_log_headers(ofl.read(297))
            pre = perf_counter()
            values = get_values(ofl)
            post = perf_counter()

        print("Values:")
        for i, v in enumerate(values):
            print("\t", headers[i][0], ": ", v)
        print("Read in {:0.9f} sec".format(post - pre))

    else:
        print("Nope")


if __name__ == "__main__":
    main()
