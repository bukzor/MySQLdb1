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
        with self.assertRaisesRegex(
            TypeError,
            "^not all arguments converted during string formatting$",
        ):
            five.bytemod(b'foo %s %s', (b'bar', b'baz', b'quux'))

    def test_too_few(self):
        with self.assertRaisesRegex(
            TypeError,
            "^not enough arguments for format string$",
        ):
            five.bytemod(b'foo %s %s', (b'bar'))

    def test_wrong_format(self):
        with self.assertRaisesRegex(
            TypeError,
            r"^unsupported format character 'Y' \(0x59\) at index 5$",
        ):
            five.bytemod(b'foo %Y', (b'bar'))

    def test_double_percent(self):
        self.assertEqual(
            b"foo bar %s",
            five.bytemod(b'foo %s %%s', b'bar')
        )
