from __future__ import unicode_literals
from __future__ import explicit_encoding
from five import b
"""MySQLdb - A DB API v2.0 compatible interface to MySQL.

This package is a wrapper around _mysql, which mostly implements the
MySQL C API.

connect() -- connects to server

See the C API specification and the MySQL documentation for more info
on other items.

For information on how MySQLdb handles type conversion, see the
MySQLdb.converters module.

"""

__revision__ = """$Revision$"""[11:-2]
import MySQLdb.release

import _mysql

__author__ = MySQLdb.release.__author__
__version__ = MySQLdb.release.__version__

if MySQLdb.release.version_info != _mysql.version_info:
    raise ImportError(
        "this is MySQLdb version %s, but _mysql is version %r" %
        (MySQLdb.release.version_info, _mysql.version_info)
    )

threadsafety = 1
apilevel = "2.0"
paramstyle = "format"

from _mysql import (
    DataError, DatabaseError, Error, IntegrityError, InterfaceError,
    InternalError, MySQLError, NULL, NotSupportedError, OperationalError,
    ProgrammingError, Warning, debug, escape,
    escape_dict, escape_sequence, escape_string, get_client_info,
    string_literal, version_info,
)
from MySQLdb.constants import FIELD_TYPE
from MySQLdb.times import Date, Time, Timestamp, \
    DateFromTicks, TimeFromTicks, TimestampFromTicks

try:
    frozenset
except NameError:
    from sets import ImmutableSet as frozenset


class DBAPISet(frozenset):

    """A special type of set for which A == x is true if A is a
    DBAPISet and x is a member of that set."""

    def __eq__(self, other):
        if isinstance(other, DBAPISet):
            return not self.difference(other)
        return other in self


STRING = DBAPISet([FIELD_TYPE.ENUM, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING])
BINARY = DBAPISet([
    FIELD_TYPE.BLOB, FIELD_TYPE.LONG_BLOB, FIELD_TYPE.MEDIUM_BLOB,
    FIELD_TYPE.TINY_BLOB,
])
NUMBER = DBAPISet([
    FIELD_TYPE.DECIMAL, FIELD_TYPE.DOUBLE, FIELD_TYPE.FLOAT, FIELD_TYPE.INT24,
    FIELD_TYPE.LONG, FIELD_TYPE.LONGLONG, FIELD_TYPE.TINY, FIELD_TYPE.YEAR,
])
DATE = DBAPISet([FIELD_TYPE.DATE, FIELD_TYPE.NEWDATE])
TIME = DBAPISet([FIELD_TYPE.TIME])
TIMESTAMP = DBAPISet([FIELD_TYPE.TIMESTAMP, FIELD_TYPE.DATETIME])
DATETIME = TIMESTAMP
ROWID = DBAPISet()


def test_DBAPISet_set_equality():
    assert STRING == STRING


def test_DBAPISet_set_inequality():
    assert STRING != NUMBER


def test_DBAPISet_set_equality_membership():
    assert FIELD_TYPE.VAR_STRING == STRING


def test_DBAPISet_set_inequality_membership():
    assert FIELD_TYPE.DATE != STRING


def Binary(x):
    return b(x)


def Connect(*args, **kwargs):
    """Factory function for connections.Connection."""
    from MySQLdb.connections import Connection
    return Connection(*args, **kwargs)

connect = Connection = Connect

__all__ = [
    'BINARY', 'Binary', 'Connect', 'Connection', 'DATE', 'Date', 'Time',
    'Timestamp', 'DateFromTicks', 'TimeFromTicks', 'TimestampFromTicks',
    'DataError', 'DatabaseError', 'Error', 'FIELD_TYPE', 'IntegrityError',
    'InterfaceError', 'InternalError', 'MySQLError', 'NULL', 'NUMBER',
    'NotSupportedError', 'DBAPISet', 'OperationalError', 'ProgrammingError',
    'ROWID', 'STRING', 'TIME', 'TIMESTAMP', 'Warning', 'apilevel', 'connect',
    'connections', 'constants', 'converters', 'cursors', 'debug', 'escape',
    'escape_dict', 'escape_sequence', 'escape_string', 'get_client_info',
    'paramstyle', 'string_literal', 'threadsafety', 'version_info',
]
