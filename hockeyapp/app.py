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

    NOTES_TEXTILE = 0
    NOTES_MARKDOWN = 1

    STATUS_FORBIDDEN = 0
    STATUS_AVAILABLE = 0

    def list(self):
        """List all apps for the API token, including owned apps, developer
        apps, member apps, and tester apps.

        :rtype: list

        """
        return self._get(uri_parts=['apps'], key='apps')

    def _check_public_identifier(self, value):
        """Check the public identifier value passed in and ensure it's the
        proper type of value.

        :param str value: The public identifier for the application
        :raises: ValueError

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

        :param str public_identifier: The public identifier for the application
        :rtype: list
        :raises: ValueError

        """
        self._check_public_identifier(public_identifier)
        return self._get(uri_parts=['apps', str(public_identifier),
                                    'statistics'])

    def upload(self, public_identifier, ipa_file=None, dsym_file=None,
               notes=None, notes_type=None, notify=False, status=1,
               mandatory=None, tags=None, commit_sha=None,
               build_server_url=None, repository_url=None):
        """Upload a new version of an application to HockeyApp. There must be
        either a ipa file or dsym file specified.

        :param str public_identifier: The public identifier for the application
        :param str ipa_file: Path to a ipa file to upload (optional)
        :param str dsym_file: Path to a dsym file to upload (optional)
        :param str notes: Notes for testers (optional)
        :param int notes_type: The type of formatting for the notes (0, 1)
        :param bool notify: Notify testers (optional)
        :param int status: Download status (1, 2))
        :param bool mandatory: Set version as mandatory (optional)
        :param list tags: a list of tags to apply to the version (optional)
        :param str commit_sha: The SCM commit sha for the version (optional)
        :param str build_server_url: URL of the build job (optional)
        :param str repository_url: URL to source repository (optional)
        :raises: ValueError

        """
        pass

    def versions(self, public_identifier):
        """Get statistics about downloads, installs, and crashes for all
        versions for an application.

        :param str public_identifier: The public identifier for the application
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
