"""
Implements an object for calling the CrashLog and Description API

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2011-09-13'

from . import api

class CrashLog(api.APIRequest):
    """This API lets you query a single crash log or description."""

    def __init__(self, api_key, app_id, crash_id, format='log'):
        """Create the CrashLog request object.

        :param api_key: HockeyApp API key
        :type api_key: str
        :param app_id: The HockeyApp Application Identifier
        :type api_key: str
        :param crash_id: The HocketApp Crash ID
        :type crash_id: str
        :param format: The response format (log/text)
        :type format: str

        """
        api.APIRequest.__init__(self, api_key)
        self._key = 'crash'
        self._app_id = app_id
        self._crash_id = crash_id
        self._format = format

    @property
    def parameters(self):
        """Returns the request parameters

        :returns: dict

        """
        return {'format': self._format}

    @property
    def path(self):
        """Returns the request path

        :returns: str

        """
        return api.BASE_URI + 'apps/%s/crashes/%s' % \
                              (self._app_id, self._crash_id)
