"""five: six, redux"""
# pylint:disable=invalid-name,redefined-builtin
str = str
bytes = bytes

PY2 = (str is bytes)
PY3 = (str is not bytes)

# provide a symettrical `text` type to `bytes`
if PY2:
    text = unicode
else:
    text = str


def n(obj):
    """Produce a native string.

    Similar in behavior to str(), but uses US-ASCII encoding when necessary.
    """
    if isinstance(obj, str):
        return obj
    elif PY2 and isinstance(obj, text):
        return obj.encode('US-ASCII')
    elif PY3 and isinstance(obj, bytes):
        return obj.decode('US-ASCII')
    else:
        return str(obj)


def u(obj):
    """Produces text.

    Similar in behavior to str() in python3 or unicode() in python2,
    but uses US-ASCII encoding when necessary.
    """
    if isinstance(obj, text):
        return obj
    elif isinstance(obj, bytes):
        return obj.decode('US-ASCII')
    else:
        return text(obj)


def b(obj):
    r"""Produces bytes.

    Similar in behavior to bytes(), but uses latin1 encoding when necessary.
    This is so that b('\x00\xFF') == future.bytes([0, 255])
    """
    if isinstance(obj, bytes):
        return obj
    elif isinstance(obj, text):
        # TODO: how come we don't actually need latin1??
        return obj.encode('US-ASCII')
    else:
        return text(obj).encode('US-ASCII')


def udict(*args, **kwargs):
    """Similar to dict(), but keyword-keys are text."""
    kwargs = dict([
        (u(key), val)
        for key, val in kwargs.items()
    ])

    return dict(*args, **kwargs)

def ndict(*args, **kwargs):
    """Similar to dict(), but keyword-keys are forced to native strings."""
    # I hate this :(
    kwargs = dict([
        (n(key), val)
        for key, val in kwargs.items()
    ])

    return dict(*args, **kwargs)

def open(*args, **kwargs):
    """Override the builtin open() to return text and use utf8 by default."""
    import io
    kwargs.setdefault('encoding', 'UTF-8')
    return io.open(*args, **kwargs)
