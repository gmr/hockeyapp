"""
Implements an object for calling the CrashList API

"""
import warnings

from hockeyapp import app


class CrashList(object):
    """For backwards compatible support, will remove in 0.5.0"""

    def __init__(self, api_token, app_id, page_id):
        warnings.warn('Deprecated for hockeyapp.Applications',
                      DeprecationWarning)
        self.app = app.Application(api_token, app_id)
        self._page_id = page_id

    def execute(self):
        warnings.warn('Deprecated for hockeyapp.Applications',
                      DeprecationWarning)
        return self.app.crash_groups(offset=self._page_id).reasons
