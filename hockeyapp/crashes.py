"""
Implements an object for calling the CrashList API

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2011-09-13'

import urllib
from . import api

class CrashList(api.APIRequest):
    """This API lets you receive the list of crashes for an app."""

    def __init__(self, api_key, app_id, page=1):
        """Create the CrashLog request object.

        :param api_key: HockeyApp API key
        :type api_key: str
        :param app_id: The HockeyApp Application Identifier
        :type api_key: str
        :param page: The page offset
        :type page: int

        """
        api.APIRequest.__init__(self, api_key)
        self._key = None
        self._app_id = app_id
        self._page = page

    @property
    def parameters(self):
        """Returns the request parameters

        :returns: dict

        """
        return {'symbolicated': 1,
                'page': self._page}

    @property
    def path(self):
        """Returns the request path

        :returns: str

        """
        params = urllib.urlencode(self.parameters)
        return api.BASE_URI + 'apps/%s/crashes?%s' % (self._app_id, params)
