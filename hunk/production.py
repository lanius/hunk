# -*- coding: utf-8 -*-

"""
hunk.production
~~~~~~~~~~~~~~~

Provides a class to configure production environment.
"""

import importlib
import os
import sys

from ._compat import urljoin, urlunsplit


class ProductionEnvironment(object):
    """Holds information for a production environment to dispatch to it."""

    def __init__(self):
        self.routes = set()

        self.scheme = 'http'
        self.hostname = 'localhost'
        self.port = 9000

    def load(self, dirpath, filename):
        filepath = os.path.join(dirpath, filename)

        if not os.path.exists(filepath):
            return  # skipped

        modname, _ = os.path.splitext(filename)
        sys.path.append(dirpath)
        config = importlib.import_module(modname)

        for attr in ['scheme', 'hostname', 'port']:
            if hasattr(config, attr):
                setattr(self, attr, getattr(config, attr))
        if hasattr(config, 'routes'):
            self.routes.update(config.routes)

    def build_url(self, path):
        base_url = urlunsplit((
            self.scheme,
            ':'.join([self.hostname, str(self.port)]),
            '', '', ''
        ))
        return urljoin(base_url, path)
