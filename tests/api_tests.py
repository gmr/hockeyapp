"""
Test the base API classes

"""
import mock
import httmock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from hockeyapp import api


class APIErrorTestCase(unittest.TestCase):

    def test_error_response_multi_repr(self):
        value = api.APIError({u'credentials': [u'no api token'],
                              u'request': [u'malformed request']})
        expectation = '<APIError [credentials, request]>'
        self.assertEqual(repr(value), expectation)

    def test_error_response_multi_str(self):
        value = api.APIError({u'credentials': [u'no api token'],
                              u'request': [u'malformed request']})
        expectation = ('[credentials]: no api token, '
                       '[request]: malformed request')
        self.assertEqual(str(value), expectation)

    def test_error_response_repr(self):
        value = api.APIError({u'credentials': [u'no api token']})
        expectation = '<APIError [credentials]>'
        self.assertEqual(repr(value), expectation)

    def test_error_response_str(self):
        value = api.APIError({u'credentials': [u'no api token']})
        expectation = '[credentials]: no api token'
        self.assertEqual(str(value), expectation)


class APIRequestTestCase(unittest.TestCase):

    def setUp(self):
        self.api = api.APIRequest('abcdef0123456789abcdef0123456789')

    def test_headers(self):
        self.assertDictEqual(self.api.headers,
                             {'Accept': 'application/json',
                              'X-HockeyAppToken': 'abcdef0123456789abcdef01234'
                                                  '56789'})

    def test_build_uri(self):
        expectation = 'https://rink.hockeyapp.net/api/2/test'
        self.assertEqual(self.api._build_uri(['test']), expectation)

    def test_uri_property(self):
        expectation = 'https://rink.hockeyapp.net/api/2/unset'
        self.assertEqual(self.api._uri, expectation)

    def test_get_calls_requests_get(self):
        @httmock.all_requests
        def response_content(url, request):
            headers = {u'content-type': u'application/json; charset=utf-8'}
            content = {u'status': u'success', u'app_versions': [u'foo']}
            return httmock.response(200, content, headers, None, 5, request)
        with httmock.HTTMock(response_content):
            self.assertListEqual(self.api._get(key='app_versions'), [u'foo'])



