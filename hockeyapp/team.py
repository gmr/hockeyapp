"""
Implements objects for calling Team Member APIs

"""

__author__ = 'Don Thorp'
__email__ = 'don@donthorp.net'
__since__ = '2012-03-20'

from . import api

class AppUsers(api.APIRequest):

    def __init__(self, api_key, app_id):
        """Create the AppUsers request object.

        :param api_key: HockeyApp API key
        :type api_key: str
        :param app_id: Application ID
        :type app_id: str

        """
        api.APIRequest.__init__(self, api_key)
        self._key = 'app_users'
        self._app_id = app_id

    @property
    def path(self):
        """Returns the request path

        :returns: str

        """
        return api.BASE_URI + 'apps/%s/app_users' % self._app_id 
