#!/usr/bin/env python
from __future__ import unicode_literals
#from __future__ import explicit_encoding
import five

import unittest


class test_bytemod(unittest.TestCase):

    def test_single(self):
        self.assertEqual(b'foo bar', five.bytemod(b'foo %s', b'bar'))
        self.assertEqual(b'foo bar', five.bytemod(b'foo %s', (b'bar',)))

    def test_double(self):
        self.assertEqual(
            b"foo bar baz",
            five.bytemod(b'foo %s %s', (b'bar', b'baz'))
        )

    def test_too_many(self):
        with assertRaisesExactly(
            TypeError,
            five.n("not all arguments converted during string formatting"),
        ):
            five.bytemod(b'foo %s %s', (b'bar', b'baz', b'quux'))

    def test_too_few(self):
        with assertRaisesExactly(
            TypeError,
            five.n("not enough arguments for format string"),
        ):
            five.bytemod(b'foo %s %s', (b'bar'))

    def test_wrong_format(self):
        with assertRaisesExactly(
            TypeError,
            five.n("unsupported format character 'Y' (0x59) at index 5"),
        ):
            five.bytemod(b'foo %Y', (b'bar'))

    def test_double_percent(self):
        self.assertEqual(
            b"foo bar %s",
            five.bytemod(b'foo %s %%s', b'bar')
        )


class assertRaisesExactly(object):
    # quasi-backported from 3.4 assertRaisesRegex
    def __init__(self, exc_type, exc_message):
        self.exc_type = exc_type
        self.exc_message = exc_message

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            try:
                exc_name = self.exc_type.__name__
            except AttributeError:
                exc_name = str(self.exc_type)
            raise AssertionError("{} not raised".format(exc_name))
        if not exc_type is self.exc_type:
            # let unexpected exceptions pass through
            return False

        if str(exc_value) != self.exc_message:
            raise AssertionError('{!r} does not match {!r}'.format(
                     self.exc_message, exc_value))

        return True
