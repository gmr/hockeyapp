
from hockeyapptest import HockeyAppTestCase

from .hockeyapp import version
from .. import api

class TestVersionAPI(HockeyAppTestCase):

    def test_list_failures(self):
        
        config = self.test_config

        version_list = version.AppVersions(config.api_key_read_only, None)
        self.assertIsNotNone(version_list)
        self.assertRaises(api.APIError, version_list.execute)

        try:
            version_list.execute()
        except api.APIError as e:
            self.assertRegexpMatches(str(e.value), "not found")

        version_list = version.AppVersions(config.api_key_read_write, None)
        self.assertIsNotNone(version_list)
        self.assertRaises(api.APIError, version_list.execute)

        try:
            version_list.execute()
        except api.APIError as e:
            self.assertRegexpMatches(str(e.value), "not found")

    def test_list(self):

        config = self.test_config

        version_list = version.AppVersions(config.api_key_read_write, config.app_id);
        versions = version_list.execute();

        #print repr(versions)
        self.assertIsInstance(versions, list)

    def test_delete_failures(self):

        config = self.test_config

        version_delete = version.AppVersionDelete(config.api_key_read_only, config.app_id, None);
        
        self.assertIsNotNone(version_delete)
        self.assertRaises(api.APIError, version_delete.execute)

        try:
            version_delete.execute()
        except api.APIError as e:
            self.assertRegexpMatches(str(e.value), "read only")

        version_delete = version.AppVersionDelete(config.api_key_read_write, config.app_id, None);
        
        self.assertIsNotNone(version_delete)
        self.assertRaises(api.APIError, version_delete.execute)

        try:
            version_delete.execute()
        except api.APIError as e:
            self.assertRegexpMatches(str(e.value), "not found")

