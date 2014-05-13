from __future__ import unicode_literals
from __future__ import explicit_encoding
from future import standard_library
standard_library.install_hooks()

import five
from future.builtins import bytes
from future.builtins import filter
from future.builtins import int
from future.builtins import str
"""MySQLdb type conversion module

This module handles all the type conversions for MySQL. If the default
type conversions aren't what you need, you can make your own. The
dictionary conversions maps some kind of type to a conversion function
which returns the corresponding value:

Key: FIELD_TYPE.* (from MySQLdb.constants)

Conversion function:

    Arguments: string

    Returns: Python object

Key: Python type object (from types) or class

Conversion function:

    Arguments: Python object of indicated type or class AND
               conversion dictionary

    Returns: SQL literal value

    Notes: Most conversion functions can ignore the dictionary, but
           it is a required parameter. It is necessary for converting
           things like sequences and instances.

Don't modify conversions if you can avoid it. Instead, make copies
(with the copy() method), modify the copies, and then pass them to
MySQL.connect().

"""

from _mysql import string_literal, escape_sequence, escape_dict, NULL
from MySQLdb.constants import FIELD_TYPE, FLAG
from MySQLdb.times import (
    DateTime2literal, DateTimeDelta2literal, mysql_timestamp_converter,
    DateTime_or_None, TimeDelta_or_None, Date_or_None,
)
from datetime import datetime, timedelta


from array import array
from decimal import Decimal

try:
    set
except NameError:
    from sets import Set as set


def Bool2Bytes(s, d):
    return str(int(s))


def Bytes2Set(s):
    return set([i for i in s.split(',') if i])


def Set2Bytes(s, d):
    return string_literal(','.join(s), d)


def Thing2Bytes(s, d):
    """Convert something into a string via str()."""
    return str(s).encode('UTF-8')


def Unicode2Bytes(s, d):
    """Convert a unicode object to a string using the default encoding.
    This is only used as a placeholder for the real function, which
    is connection-dependent.
    """
    return s.encode('US-ASCII')

Long2Int = Thing2Bytes


def Float2Bytes(o, d):
    return ('%.15g' % o).encode('US-ASCII')


def None2NULL(o, d):
    """Convert None to NULL."""
    return NULL  # duh


def Bytes2Literal(o, d):
    """Convert something into a SQL string literal.  If using
    MySQL-3.23 or newer, string_literal() is a method of the
    _mysql.MYSQL object, and this function will be overridden with
    that method when the connection is created.
    """
    return string_literal(o, d)


def Thing2Literal(o, d):
    return Bytes2Literal(Thing2Bytes(o, d), d)


def Object2Literal(o, d):
    """Convert an Instance to a string representation.  If the __str__()
    method produces acceptable output, then you don't need to add the
    class to conversions; it will be handled by the default
    converter. If the exact class is not found in d, it will use the
    first class it can find for which o is an instance.
    """
    cls = type(o)
    for supercls in type.mro(cls)[1:-1]:
        if supercls in d:
            convertor = d[supercls]
            break
    else:
        convertor = Thing2Literal

    if cls is not object:
        d[cls] = convertor
    return convertor(o, d)


def char_array(s):
    return array.array('c', s)


def array2Bytes(o, d):
    return Bytes2Literal(o.tostring(), d)

def bytes2Decimal(s):
    return Decimal(s.decode('US-ASCII'))

def quote_tuple(t, d):
    return "(%s)" % (','.join(escape_sequence(t, d)))

conversions = {
    int: Thing2Bytes,
    float: Float2Bytes,
    type(None): None2NULL,
    tuple: quote_tuple,
    list: quote_tuple,
    dict: escape_dict,
    array: array2Bytes,
    bytes: Bytes2Literal,
    str: Unicode2Bytes,
    object: Object2Literal,
    bool: Bool2Bytes,
    datetime: DateTime2literal,
    timedelta: DateTimeDelta2literal,
    set: Set2Bytes,
    FIELD_TYPE.TINY: int,
    FIELD_TYPE.SHORT: int,
    FIELD_TYPE.LONG: int,
    FIELD_TYPE.FLOAT: float,
    FIELD_TYPE.DOUBLE: float,
    FIELD_TYPE.DECIMAL: bytes2Decimal,
    FIELD_TYPE.NEWDECIMAL: bytes2Decimal,
    FIELD_TYPE.LONGLONG: int,
    FIELD_TYPE.INT24: int,
    FIELD_TYPE.YEAR: int,
    FIELD_TYPE.SET: Bytes2Set,
    FIELD_TYPE.TIMESTAMP: mysql_timestamp_converter,
    FIELD_TYPE.DATETIME: DateTime_or_None,
    FIELD_TYPE.TIME: TimeDelta_or_None,
    FIELD_TYPE.DATE: Date_or_None,
    FIELD_TYPE.BLOB: [(FLAG.BINARY, five.b)],
    FIELD_TYPE.STRING: [(FLAG.BINARY, five.b)],
    FIELD_TYPE.VAR_STRING: [(FLAG.BINARY, five.b)],
    FIELD_TYPE.VARCHAR: [(FLAG.BINARY, five.b)],
}

if False: #five.PY2:
    # TODO: how come these aren't necessary?
    from types import InstanceType
    conversions.update({
        InstanceType: Object2Literal,
        # handle the non-futured types too.
        five.bytes: Bytes2Literal,  # default
        five.text: Unicode2Bytes,
    })
