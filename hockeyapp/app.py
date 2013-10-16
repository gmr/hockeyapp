"""
Implements an object for calling the Application List API

"""
from hockeyapp import api
import re
import warnings


class Application(api.APIRequest):
    """Manage an Application at Hockeyapp"""
    KEY = 'app_versions'
    PI_PATTERN = re.compile(r'[a-f0-9]{32}')

    def list(self):
        """List all apps for the API token, including owned apps, developer
        apps, member apps, and tester apps.

        :rtype: list

        """
        return self._get(uri_parts=['apps'], key='apps')

    def _check_public_identifier(self, value):
        """Check the public identifier value passed in and ensure it's the
        proper type of value.

        """
        if isinstance(value, int) or value.isdigit():
            raise ValueError('Must pass in the public_identifier value, '
                             'not the numeric app id value')
        if not self.PI_PATTERN.match(value):
            raise ValueError('public_identifier is a 32 character hex digest '
                             'hash value')

    def statistics(self, public_identifier):
        """Get statistics about downloads, installs, and crashes for all
        versions for an application.

        :param str public_identifier: The public_identifier for an app
        :rtype: list
        :raises: ValueError

        """
        self._check_public_identifier(public_identifier)
        return self._get(uri_parts=['apps', str(public_identifier),
                                    'statistics'])

    def versions(self, public_identifier):
        """Get statistics about downloads, installs, and crashes for all
        versions for an application.

        :param str public_identifier: The public_identifier for an app
        :rtype: list
        :raises: ValueError

        """
        self._check_public_identifier(public_identifier)
        return self._get(uri_parts=['apps', str(public_identifier),
                                    'app_versions'])

# Deprecated classes for transitional support, to be removed in future versions

class AppList(Application):
    """Return the application list for a given token"""

    def __init__(self, token):
        warnings.warn('Deprecated for hockeyapp.Applications',
                      DeprecationWarning)
        super(AppList, self).__init__(token)

    def execute(self):
        self.list()
