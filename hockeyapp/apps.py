"""
Implements an object for calling the Application List API

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2011-09-13'

from . import api

class AppList(api.APIRequest):

    def __init__(self, api_key):
        """Create the AppList request object.

        :param api_key: HockeyApp API key
        :type api_key: str

        """
        api.APIRequest.__init__(self, api_key)
        self._key = 'apps'

    @property
    def path(self):
        """Returns the request path

        :returns: str

        """
        return api.BASE_URI + 'apps'
