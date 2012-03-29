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

    @property
    def first_name(self):
        """Returns the user's first name

        :returns: str

        """
        return self._first_name

    @first_name.setter
    def first_name(self, name):
        """set the user's first name

        :param name: name
        :type name: str

        """
        self._first_name = name

    @property
    def last_name(self):
        """Returns the user's last name

        :returns: str

        """
        return self._last_name

    @last_name.setter
    def last_name(self, name):
        """set the user's last name

        :param name: name
        :type name: str

        """
        self._last_name = name

    @property
    def message(self):
        """Returns the message to send to the user in the invitation

        :returns: str

        """
        return self._message 

    @message.setter
    def message(self, msg):
        """set the message to send in the invite

        :param msg: the message
        :type msg: str

        """
        self._message = msg

    @property
    def role(self):
        """Returns the user's role constant

        :returns: int

        """
        return self._role

    @role.setter
    def role(self, role):
        """set the user's role. One of 0 - owner, 1 - developer, 2 - member, 3 - tester

        :param role: role constant
        :type role: int

        """

        self._role = int(role)

    @property
    def tags(self):
        """Returns the user's tags

        :returns: str

        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """set the user's tags

        :param tags: tags (comma delimited)
        :type tags: str

        """
        self._tags = tags

class AppDeleteUser(api.APIRequest):

    def __init__(self, api_key, app_id, user_id):
        """Create the AppDeleteUser request object.

        :param api_key: HockeyApp API key
        :type api_key: str
        :param app_id: Application ID
        :type app_id: str
        :param user_id: User id
        :type user_id: int

        """
        api.APIRequest.__init__(self, api_key)
        self._key = 'app_users'
        self._app_id = app_id
        self._user_id = user_id
        self._method = 'DELETE'

    @property
    def path(self):
        """Returns the request path

        :returns: str

        """
        return api.BASE_URI + 'apps/%s/app_users/%s' % (self._app_id, self._user_id) 

