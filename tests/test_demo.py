# -*- coding: utf-8 -*-

import json
from os.path import join, dirname, realpath

import mock

from ._compat import json_text

from hunk.server import set_config, set_production_environment, app


PROJECT_ROOT = dirname(dirname(realpath(__file__)))
DEMO_ROOT = join(PROJECT_ROOT, 'demo')

SERVER_HOSTNAME = 'localhost'
SERVER_PORT = 8080


class Base(object):

    def request(self, method, path):
        rv = getattr(self.app, method)(path)
        try:
            data = json.loads(json_text(rv))
        except ValueError:
            data = None
        return data, rv.headers, rv.status_code

    def get(self, path):
        return self.request('get', path)

    def post(self, path):
        return self.request('post', path)


class TestSimple(Base):

    def setup(self):
        root = join(DEMO_ROOT, 'simple')
        set_config(root, SERVER_HOSTNAME, SERVER_PORT)
        self.app = app.test_client()

    def test_get_a_resource(self):
        data, _, status = self.get('/members/100')
        assert data['name'] == 'Dorothy'
        assert status == 200

        data, _, status = self.get('/members/300.json')
        assert data['name'] == 'Hunk'
        assert status == 200

        _, _, status = self.get('/members/1000')
        assert status == 404

    def test_get_resources_from_directory(self):
        def assert_members(data, _, status):
            assert len(data) == 9
            assert 'Hunk' in map(lambda d: d['name'], data)
            assert status == 200

        assert_members(*self.get('/members'))
        assert_members(*self.get('/members/'))

    def test_get_resources_from_file(self):
        def assert_sounds(data, _, status):
            assert len(data) == 9
            assert 'Over The Rainbow' in map(lambda d: d['title'], data)
            assert status == 200

        assert_sounds(*self.get('/sounds'))
        assert_sounds(*self.get('/sounds/'))

    def test_post_a_resource(self):
        def assert_members(data, _, status):
            assert data['result'] == 'success'
            assert status == 200

        assert_members(*self.post('/members'))
        assert_members(*self.post('/members/'))


class TestMetadata(Base):

    def setup(self):
        root = join(DEMO_ROOT, 'metadata')
        set_config(root, SERVER_HOSTNAME, SERVER_PORT)
        self.app = app.test_client()

    def test_status(self):
        def assert_forbidden(_, _h, status):
            assert status == 403

        assert_forbidden(*self.get('/forbidden'))
        assert_forbidden(*self.get('/forbidden/record'))

    def test_headers(self):
        def assert_allow(_, headers, status):
            assert headers.get('Server') == 'hunk!'
            assert headers.get('Allow') == 'GET'
            assert status == 200

        assert_allow(*self.get('/allow/'))
        assert_allow(*self.get('/allow/record'))


class TestProxyForProduction(Base):

    def setup(self):
        root = join(DEMO_ROOT, 'production')
        set_config(root, SERVER_HOSTNAME, SERVER_PORT)
        set_production_environment(root, 'production_conf.py')
        self.app = app.test_client()

    def test_get_mock_resource(self):
        def assert_mock(data, _, status):
            assert 'hunk' in data['message']
            assert status == 200

        assert_mock(*self.get('/available/1'))
        assert_mock(*self.get('/available/3'))

    def test_get_production_resource(self):
        def assert_production(path):
            with mock.patch('requests.get', return_value=None) as m:
                self.get(path)
                url = m.call_args[0][0]
                assert url == 'http://localhost:9000' + path

        assert_production('/available/2')
        assert_production('/available/4')
