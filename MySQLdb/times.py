from __future__ import unicode_literals
#from __future__ import explicit_encoding
from __future__ import division
from future.builtins import map
from future.builtins import int
from five import n
"""times module

Use Python datetime module to handle date and time columns."""

from time import localtime
from datetime import date, datetime, time, timedelta
from _mysql import string_literal


def DateFromTicks(ticks):
    """Convert UNIX ticks into a date instance."""
    return date(*localtime(ticks)[:3])


def TimeFromTicks(ticks):
    """Convert UNIX ticks into a time instance."""
    return time(*localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    """Convert UNIX ticks into a datetime instance."""
    return datetime(*localtime(ticks)[:6])

format_TIME = format_DATE = str


def format_TIMEDELTA(v):
    seconds = int(v.seconds) % 60
    minutes = (v.seconds // 60) % 60
    hours = (v.seconds // 3600) % 24
    return '%d %d:%d:%d' % (v.days, hours, minutes, seconds)


def format_TIMESTAMP(d):
    return d.isoformat(n(" "))


def DateTime_or_None(s):
    if b' ' in s:
        sep = b' '
    elif b'T' in s:
        sep = b'T'
    else:
        return Date_or_None(s)

    d, t = s.split(sep, 1)
    if b'.' in t:
        t, ms = t.split(b'.', 1)
        ms = ms.ljust(6, b'0')
    else:
        ms = 0
    return datetime(*[
        int(x) for x in d.split(b'-') + t.split(b':') + [ms]
    ])


def TimeDelta_or_None(s):
    h, m, s = s.split(b':')
    if b'.' in s:
        s, ms = s.split(b'.')
        ms = ms.ljust(6, b'0')
    else:
        ms = 0
    h, m, s, ms = int(h), int(m), int(s), int(ms)
    td = timedelta(hours=abs(h), minutes=m, seconds=s,
                   microseconds=ms)
    if h < 0:
        return -td
    else:
        return td


def Time_or_None(s):
    h, m, s = s.split(':')
    if '.' in s:
        s, ms = s.split('.')
        ms = ms.ljust(6, '0')
    else:
        ms = 0
    h, m, s, ms = int(h), int(m), int(s), int(ms)
    return time(hour=h, minute=m, second=s,
                microsecond=ms)


def Date_or_None(s):
    return date(*[
        int(x) for x in s.split(b'-', 2)
    ])


def DateTime2literal(d, c):
    """Format a DateTime object as an ISO timestamp."""
    return string_literal(format_TIMESTAMP(d), c)


def DateTimeDelta2literal(d, c):
    """Format a DateTimeDelta object as a time."""
    return string_literal(format_TIMEDELTA(d), c)


def mysql_timestamp_converter(s):
    """Convert a MySQL TIMESTAMP to a datetime object."""
    # MySQL>4.1 returns TIMESTAMP in the same format as DATETIME
    if s[4:5] == b'-':
        return DateTime_or_None(s)
    s = s + b"0" * (14 - len(s))  # padding
    parts = list(map(int, [_f for _f in (s[:4], s[4:6], s[6:8],
                                   s[8:10], s[10:12], s[12:14]) if _f]))
    return datetime(*parts)
