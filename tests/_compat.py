# -*- coding: utf-8 -*-

import sys


PY2 = sys.version_info[0] == 2


if not PY2:
    json_text = lambda rv: rv.data.decode(rv.charset)

else:
    json_text = lambda rv: rv.data
