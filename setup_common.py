from __future__ import unicode_literals
from __future__ import explicit_encoding
from five import u, open
try:
    # Python 2.x
    from ConfigParser import SafeConfigParser
except ImportError:
    # Python 3.x pylint:disable=import-error
    from configparser import ConfigParser as SafeConfigParser


def get_metadata_and_options():
    config = SafeConfigParser()
    for fname in ['metadata.cfg', 'site.cfg']:
        config.readfp(open(fname), fname)

    metadata = dict(config.items('metadata'))
    options = dict(config.items('options'))

    metadata['py_modules'] = metadata['py_modules'].split()
    metadata['classifiers'] = metadata['classifiers'].split()

    return metadata, options


def enabled(options, option):
    value = options[option]
    s = value.lower()
    if s in ('yes', 'true', '1', 'y'):
        return True
    elif s in ('no', 'false', '0', 'n'):
        return False
    else:
        raise ValueError("Unknown value %s for option %s" % (value, option))


def create_release_file(metadata):
    rel = open("MySQLdb/release.py", 'w')
    rel.write("""\
from __future__ import unicode_literals
from __future__ import explicit_encoding

__author__ = "%(author)s <%(author_email)s>"
version_info = %(version_info)s
__version__ = "%(version)s"
""" % metadata)
    rel.close()
