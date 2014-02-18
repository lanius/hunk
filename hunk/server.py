# -*- coding: utf-8 -*-

"""
hunk.server
~~~~~~~~~~~

Provides mock server that has JSON API.
"""

import argparse
import os

from flask import Flask, request, make_response, abort
import requests

from .resource import load_resource
from .production import ProductionEnvironment


METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']


app = Flask(__name__)

config = {
    'RESOURCE_ROOT': os.getcwd(),
    'SERVER_HOSTNAME': 'localhost',
    'SERVER_PORT': 8080
}

prod_env = ProductionEnvironment()


def get_response_from_proxy(method, url, data, headers):
    rv = getattr(requests, method)(url, data=data, headers=headers)
    response = make_response(rv.text, rv.status_code)
    response.headers.clear()
    for k, v in rv.headers.items():
        response.headers.add_header(k, v)
    return response


def get_response_from_resource(resource):
    response = make_response(resource.json, resource.status_code)
    response.headers['Content-Type'] = 'application/json'
    for key, value in resource.headers.items():
        response.headers[key] = value
    return response


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/', methods=METHODS)
def index():
    return resources('/')


@app.route('/<path:path>', methods=METHODS)
def resources(path):
    method = request.method.lower()

    if request.path in prod_env.routes:
        url = prod_env.build_url(path)
        return get_response_from_proxy(
            method, url, request.data, request.headers)

    rpath = os.path.join(
        config['RESOURCE_ROOT'], method, *path.rstrip('/').split('/'))
    r = load_resource(rpath)
    if r:
        return get_response_from_resource(r)
    else:
        abort(404)


def set_config(root, hostname, port):
    config['RESOURCE_ROOT'] = root
    config['SERVER_HOSTNAME'] = hostname
    config['SERVER_PORT'] = port


def set_production_environment(dirpath, py_filename):
    prod_env.load(dirpath, py_filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', default=os.getcwd())
    parser.add_argument('-n', '--hostname', default='localhost')
    parser.add_argument('-p', '--port', type=int, default=8080)
    parser.add_argument('-c', '--production', default='production_conf.py')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    set_config(args.root, args.hostname, args.port)
    set_production_environment(args.root, args.production)

    app.debug = args.debug or False

    app.run(config['SERVER_HOSTNAME'], config['SERVER_PORT'])


if __name__ == '__main__':
    main()
