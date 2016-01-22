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
    TOKEN = 'abcdef0123456789abcdef0123456789'
    APP_IDENTIFIER = 'zyxw98765'

    def setUp(self):
        self.app = app.Application(self.TOKEN)
        self.applications = app.Applications(self.TOKEN)

    def test_invalid_identifier_number(self):
        self.assertRaises(ValueError, self.app._check_app_id, 1)

    def test_invalid_identifier_format(self):
        self.assertRaises(ValueError, self.app._check_app_id, 'foo')

    @mock.patch.object(app.Applications, '_get')
    def test_list(self, get):
        self.applications.list()
        get.assert_called_with(uri_parts=['apps'])
        get.return_value.__getitem__.assert_called_with('apps')

    @mock.patch.object(app.Application, '_check_app_id')
    @mock.patch.object(app.Application, '_get')
    def test_statistics(self, get, _):
        application = app.Application(self.TOKEN, app_id=self.APP_IDENTIFIER)
        application.statistics()
        get.assert_called_with(uri_parts=['apps', self.APP_IDENTIFIER, 'statistics'])

    @mock.patch.object(app.Application, '_check_app_id')
    @mock.patch.object(app.Application, '_get')
    def test_verions(self, get, _):
        application = app.Application(self.TOKEN, app_id=self.APP_IDENTIFIER)
        application.versions()
        get.assert_called_with(uri_parts=['apps', self.APP_IDENTIFIER, 'app_versions'])
