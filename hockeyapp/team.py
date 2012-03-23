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

class AppAddUser(api.APIRequest):

    def __init__(self, api_key, app_id, email):
        """Create the AppUsers request object.

        :param api_key: HockeyApp API key
        :type api_key: str
        :param app_id: Application ID
        :type app_id: str
        :param email: User email address
        :type email: str

        """
        api.APIRequest.__init__(self, api_key)
        self._app_id = app_id
        self._method = 'POST'
        self._email = email
        self._first_name = None
        self._last_name = None
        self._message = None
        self._role = None
        self._tags = None

    @property
    def parameters(self):
        """Returns the request parameters

        :returns: dict

        """
        params = { 'email' : self._email }
        
        if not self._first_name is None: 
            params['first_name'] = self._first_name
        if not self._last_name is None:
            params['last_name'] = self._last_name
        if not self._message is None:
            params['message'] = self._message
        if not self._role is None:
            params['role'] = self._role
        if not self._tags is None:
            params['tags'] = self._tags

        return params

    @property
    def path(self):
        """Returns the request path

        :returns: str

        """
        return api.BASE_URI + 'apps/%s/app_users' % self._app_id 


