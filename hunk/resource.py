# -*- coding: utf-8 -*-

"""
hunk.resource
~~~~~~~~~~~~~

Defines classes to load and serialize resources.
"""

import json
import os
from glob import glob


def load_resource(rpath):
    """Return a resource object by path."""
    if os.path.isfile(rpath):
        return File(rpath)

    for ext in ['json']:
        fpath = '.'.join([rpath, ext])
        if os.path.isfile(fpath):
            return File(fpath)

    if os.path.isdir(rpath):
        return Directory(rpath)

    return None


class Resource(object):
    """An abstract class that represents resources of file system."""

    def load_headers(self, path):
        """Loads headers from .headers file."""
        data = self._load_metadata(path, '.headers')
        if not data:
            return {}
        return dict([
            map(lambda s: s.strip(), line.split(':'))
            for line in data.splitlines()
        ])

    def load_status_code(self, path):
        """Loads status code from .status file."""
        data = self._load_metadata(path, '.status')
        if not data:
            return 200
        return int(data)

    def _load_metadata(self, path, filename):
        fpath = os.path.join(path, filename)
        if not os.path.exists(fpath):
            return None
        with open(fpath, 'r') as f:
            return f.read()

    @property
    def json_obj(self):
        """Returns JSON object that represents this resource as Python object.
        Need to be overridden.
        """
        assert False

    @property
    def json(self):
        """Returns JSON object that represents this resource as serialized
        string.
        """
        return json.dumps(self.json_obj)


class File(Resource):
    """Represents a file."""

    def __init__(self, rpath):
        self.rpath = rpath
        parent = os.path.dirname(rpath)
        self.headers = self.load_headers(parent)
        self.status_code = self.load_status_code(parent)

    @property
    def json_obj(self):
        with open(self.rpath, 'r') as f:
            return json.load(f)


class Directory(Resource):
    """Represents a directory."""

    def __init__(self, rpath):
        self.rpath = rpath
        self.headers = self.load_headers(rpath)
        self.status_code = self.load_status_code(rpath)

    @property
    def json_obj(self):
        # exclude dot files by using glob
        content = [p for p in glob(os.path.join(self.rpath, '*'))]

        # if no content, return empty array
        if not content:
            return []

        # if all content are a file, concat and return them
        if not list(filter(os.path.isdir, content)):
            return [File(p).json_obj for p in content]

        # if directories and files exist, extend and return named object
        rv = {}
        for p in content:
            name = os.path.basename(p).rstrip('.json')
            resource_cls = File if os.path.isfile(p) else Directory
            rv[name] = resource_cls(p).json_obj
        return rv
