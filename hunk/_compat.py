# -*- coding: utf-8 -*-

"""
hunk._compat
~~~~~~~~~~~~

Some py2/py3 compatibility support.
"""

import sys


PY2 = sys.version_info[0] == 2


if not PY2:
    from urllib.parse import urljoin, urlunsplit

else:
    from urlparse import urljoin, urlunsplit


__all__ = ['urljoin', 'urlunsplit']
