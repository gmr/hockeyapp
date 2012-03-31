"""
Implements objects for calling Version APIs

"""

__author__ = 'Don Thorp'
__email__ = 'don@donthorp.net'
__since__ = '2012-03-23'

import sys
from . import api

try:
    import poster
except ImportError:
    print "You need to install poster.\n  use: sudo pip install poster\n"
    sys.exit(1)

class AppVersions(api.APIRequest):

    def __init__(self, api_key, app_id):
        """Create the AppVersions request object for developers.

        :param api_key: HockeyApp API key
        :type api_key: str
        :param app_id: Application ID
        :type app_id: str

        """
        api.APIRequest.__init__(self, api_key)
        self._key = 'app_versions'
        self._app_id = app_id

    @property
    def path(self):
        """Returns the request path

        :returns: str

        """
        return api.BASE_URI + 'apps/%s/app_versions' % self._app_id

class AppVersionDelete(api.APIRequest):

    def __init__(self, api_key, app_id, version_id, purge=False):
        """Create the AppDeleteVersion request object.

        :param api_key: HockeyApp API key
        :type api_key: str
        :param app_id: Application ID
        :type app_id: str
        :param purge: Remove permanently
        :param purge: boolean

        """
        api.APIRequest.__init__(self, api_key)
        self._method = 'DELETE'
        self._app_id = app_id
        self._version_id = version_id
        self._purge = purge

    @property
    def parameters(self):
        """Returns the request parameters

        :returns: dict

        """
        params = {}

        if (self._purge):
            params['strategy'] = 'purge'

        return params

    @property
    def path(self):
        """Returns the request path

        :returns: str

        """
        return api.BASE_URI + 'apps/%s/app_versions/%s' % (self._app_id, self._version_id)

