
from unittest2 import TestCase
import os
import sys
import yaml

class TestConfig:

    def __init__(self, data):
        self.data = data

    @property
    def api_key_read_only(self):
        return self.data["api_key_read_only"]

    @property
    def api_key_read_write(self):
        return self.data["api_key_read_write"]

    @property
    def app_id(self):
        return self.data["app_id"]

    @property
    def user(self):
        return self.data['user']

class HockeyAppTestCase(TestCase):

    def setUp(self):
        config_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'test-config.yml'))
        
        if not os.path.exists(config_file):
            print "CONFIG ERROR: Copy test-config.yml.example to test-config.yml and provide data."
            sys.exit(1)

        # print "Loading config file: %s" % config_file
        self.test_config = TestConfig(yaml.load(file(config_file, 'r')))

