"""
Implements objects for calling Version APIs

"""

__author__ = 'Don Thorp'
__email__ = 'don@donthorp.net'
__since__ = '2012-03-23'

import sys
from . import api


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

class AppVersionAdd(api.APIRequest):

    NOTE_TYPE_MARKDOWN = 1
    NOTE_TYPE_TEXTILE = 0

    def __init__(self, api_key, app_id, ipa, dsym=None, notes = None, notes_type = 1, notify = True, downloadable = True, tags = None):
        """Create the AppVersionAdd request object.

        :param api_key: HockeyApp API key
        :type api_key: str
        :param app_id: Application ID
        :type app_id: str
        :param ipa: File to upload
        :type ipa: File
        :param dsym: .dSYMzip or mapping.txt. (optional)
        :type dsym: File
        :param notes: release notes (optional)
        :type notes: str
        :param notes_type: 0 - Textile, 1 - Markdown. Default: 1. (optional)
        :type notes_type: int
        :param notify: Notify tester. Default: True. (optional)
        :type notify: bool
        :param downloadable: Allow download Default: True. (optional)
        :type downloadable: bool
        :param tags: Restrict download to comma separated list of tags
        :type tags: str

        """
        api.APIRequest.__init__(self, api_key)
        self._method = 'POST'
        self._app_id = app_id
        self._ipa = ipa
        self._dsym = dsym
        self._notes = notes
        self._notes_type = notes_type
        self.notify = notify
        self.downloadable = downloadable
        self._tags = tags

    @property
    def parameters(self):
        """Returns the request parameters

        :returns: dict

        """
        params = {}

        if self._ipa:
            params['ipa'] = self._ipa

        if self._dsym:
            params['dsym'] = self._dsym

        if self._notes:
            params['notes'] = self._notes
            params['notes_type'] = self._notes_type

        params['notify'] = self._notify
        params['status'] = self._status

        if self._tags:
            params['tags'] = self._tags

        return params

    @property
    def path(self):
        """Returns the request path

        :returns: str

        """
        return api.BASE_URI + 'apps/%s/app_versions' % self._app_id

    @property
    def dsym(self):
        return self._dsym

    @dsym.setter
    def dsym(self, f):
        self._dsym = f

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, note):
        self._notes = note

    @property
    def notes_type(self):
        return self._notes_type

    @notes_type.setter
    def notes_type(self, note_type):
        self._notes_type = note_type

    @property
    def notify(self):
        return self._notify == 1

    @notify.setter
    def notify(self, v):
        self._notify = 1 if v else 0

    @property
    def downloadable(self):
        return self._status == 2

    @downloadable.setter
    def downloadable(self, v):
        self._status = 2 if v else 1

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags
