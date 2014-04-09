#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import explicit_encoding
from five import n, text

import os
import sys

import distutils.errors
import setuptools

if not hasattr(sys, "hexversion") or sys.hexversion < 0x02040000:
    raise distutils.errors.DistutilsError("Python 2.4 or newer is required")

if os.name == n("posix"):
    from setup_posix import get_config
else:  # assume windows
    from setup_windows import get_config

def maybe_native_string(x):
    if isinstance(x, (bytes, text)):
        return n(x)
    else:
        return x

def native_dict(d):
    """Setuptools asserts native strings."""
    return dict(
        (n(key), [maybe_native_string(v) for v in val])
            if isinstance(val, list) else
        (n(key), maybe_native_string(val))
        for key, val in d.items()
    )

metadata, options = get_config()
metadata['ext_modules'] = [
    setuptools.Extension(sources=[n('_mysql.c')], **native_dict(options))]
metadata['long_description'] = metadata['long_description'].replace(r'\n', '')
setuptools.setup(**native_dict(metadata))
