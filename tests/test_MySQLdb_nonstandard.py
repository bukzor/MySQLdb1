from __future__ import unicode_literals
#from __future__ import explicit_encoding

import unittest

import _mysql
import MySQLdb
from MySQLdb.constants import FIELD_TYPE
from configdb import connection_factory
from five import text
import warnings
warnings.simplefilter("ignore")


class TestDBAPISet(unittest.TestCase):
    def test_set_equality(self):
        self.assertTrue(MySQLdb.STRING == MySQLdb.STRING)

    def test_set_inequality(self):
        self.assertTrue(MySQLdb.STRING != MySQLdb.NUMBER)

    def test_set_equality_membership(self):
        self.assertTrue(FIELD_TYPE.VAR_STRING == MySQLdb.STRING)

    def test_set_inequality_membership(self):
        self.assertTrue(FIELD_TYPE.DATE != MySQLdb.STRING)


class CoreModule(unittest.TestCase):
    """Core _mysql module features."""

    def test_NULL(self):
        """Should have a NULL constant."""
        self.assertEqual(_mysql.NULL, b'NULL')

    def test_version(self):
        """Version information sanity."""
        self.assertTrue(isinstance(_mysql.__version__, text))

        self.assertTrue(isinstance(_mysql.version_info, tuple))
        self.assertEqual(len(_mysql.version_info), 5)

    def test_client_info(self):
        self.assertTrue(isinstance(_mysql.get_client_info(), text))

    def test_thread_safe(self):
        self.assertTrue(isinstance(_mysql.thread_safe(), int))

    def test_installation_path(self):
        from os.path import dirname
        self.assertEqual(dirname(_mysql.__file__), dirname(dirname(MySQLdb.__file__)))


class CoreAPI(unittest.TestCase):
    """Test _mysql interaction internals."""

    def setUp(self):
        self.conn = connection_factory(use_unicode=True)

    def tearDown(self):
        self.conn.close()

    def test_thread_id(self):
        tid = self.conn.thread_id()
        self.assertTrue(isinstance(tid, int),
                        "thread_id didn't return an int.")

        self.assertRaises(TypeError, self.conn.thread_id, ('evil',),
                          "thread_id shouldn't accept arguments.")

    def test_affected_rows(self):
        self.assertEquals(self.conn.affected_rows(), 0,
                          "Should return 0 before we do anything.")

    #def test_debug(self):
        ## FIXME Only actually tests if you lack SUPER
        #self.assertRaises(
        #   MySQLdb.OperationalError,
        #   self.conn.dump_debug_info
        #)

    def test_charset_name(self):
        self.assertTrue(isinstance(self.conn.character_set_name(), text),
                        "Should return a string.")

    def test_host_info(self):
        self.assertTrue(isinstance(self.conn.get_host_info(), text),
                        "Should return a string.")

    def test_proto_info(self):
        self.assertTrue(isinstance(self.conn.get_proto_info(), int),
                        "Should return an int.")

    def test_server_info(self):
        self.assertTrue(isinstance(self.conn.get_server_info(), text),
                        "Should return an str.")
