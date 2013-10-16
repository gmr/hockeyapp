"""
Test the Application class

"""
import mock
import httmock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from hockeyapp import app


class ApplicationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.Application('abcdef0123456789abcdef0123456789')

    def test_invalid_identifier_number(self):
        self.assertRaises(ValueError, self.app._check_public_identifier, 1)

    def test_invalid_identifier_format(self):
        self.assertRaises(ValueError, self.app._check_public_identifier, 'foo')

    @mock.patch.object(app.Application, '_get')
    def test_list(self, get):
        self.app.list()
        get.assert_called_with(uri_parts=['apps'], key='apps')

    @mock.patch.object(app.Application, '_get')
    def test_statistics(self, get):
        identifier = 'abcdef0123456789abcdef0123456789'
        self.app.statistics(identifier)
        get.assert_called_with(uri_parts=['apps', identifier, 'statistics'])

    @mock.patch.object(app.Application, '_get')
    def test_verions(self, get):
        identifier = 'abcdef0123456789abcdef0123456789'
        self.app.versions(identifier)
        get.assert_called_with(uri_parts=['apps', identifier, 'app_versions'])
