"""
Implements an object for calling the Application List API

"""
import collections
import os
import re
import tempfile
import warnings
import zipfile

from hockeyapp import api

Crashes = collections.namedtuple('Crashes', 'crashes,total_entries,'
                                            'total_pages,current_page,'
                                            'per_page')

CrashGroups = collections.namedtuple('CrashGroup', 'reasons,total_entries,'
                                                   'total_pages,current_page,'
                                                   'per_page')

Feedback = collections.namedtuple('Feedback', 'feedback,total_entries,'
                                              'total_pages,current_page,'
                                              'items_per_page')


class Applications(api.APIRequest):
    """Top level management of apps"""
    KEY = 'apps'

    def list(self):
        """List all apps for the API token, including owned apps, developer
        apps, member apps, and tester apps.

        :rtype: list

        """
        return self._get(uri_parts=['apps'])['apps']


class Application(api.APIRequest):
    """Manage an Application at HockeyApp"""

    # Pattern for validating the APP ID value
    APP_ID_PATTERN = re.compile(r'[a-f0-9]{32}')

    CRASH_STATUS_OPEN = 0
    CRASH_STATUS_RESOLVED = 1
    CRASH_STATUS_IGNORED = 2

    NOTES_TEXTILE = 0
    NOTES_MARKDOWN = 1

    PLATFORM_IOS = 'iOS'
    PLATFORM_ANDROID = 'Android'
    PLATFORM_OSX = 'Mac OS'
    PLATFORM_WINDOWS_PHONE = 'Windows Phone'
    PLATFORM_CUSTOM = 'Custom'

    RELEASE_ALPHA = 2
    RELEASE_BETA = 0
    RELEASE_LIVE = 1

    STATUS_FORBIDDEN = 0
    STATUS_AVAILABLE = 0

    VALID_PLATFORMS = [PLATFORM_ANDROID, PLATFORM_CUSTOM, PLATFORM_IOS,
                       PLATFORM_OSX, PLATFORM_WINDOWS_PHONE]
    VALUE_RELEASE = [RELEASE_ALPHA, RELEASE_BETA, RELEASE_LIVE]

    def __init__(self, token, app_id=None):
        """Construct the Application object

        :param str token: The API token for the request
        :param str app_id: The App ID public identifier for an existing app
        :raises: ValueError

        """
        if app_id:
            self._check_app_id(app_id)
        self._app_id = app_id
        super(Application, self).__init__(token)

    def create(self, title, bundle_identifier, platform='iOS', release_type=0):
        """Create a new application without uploading a file.

        If specified, the platform must be one of the following values:

            - iOS [default]
            - Android
            - Mac OS
            - Windows Phone
            - Custom

        Constants for release_type:

            - Application.RELEASE_ALPHA
            - Application.RELEASE_BETA
            - Application.RELEASE_LIVE

        :param str title: The application's name
        :param str bundle_identifier: Bundle identifier on iOS or Mac OS X,
            the package name on Android, or the namespace on Windows Phone
        :param str platform: The app platform (optional)
        :param int release_type: An integer value for Alpha, Beta or Live.
        :return str: app_id public identifier

        """
        if platform not in self.VALID_PLATFORMS:
            raise ValueError('Invalid platform value')

        if release_type not in self.VALUE_RELEASE:
            raise ValueError('Invalid release value')
        response = self._post(uri_parts=['apps', 'new'],
                              data={'title': title,
                                    'bundle_identifier': bundle_identifier,
                                    'platform': platform,
                                    'release_type': release_type})
        self._app_id = response['public_identifier']
        return response['public_identifier']

    def crash_description(self, crash_id):
        """Get the crash description

        :param str crash_id: The specific crash to get
        :rtype: str
        :raise: ValueError

        """
        response = self._get(uri_parts=['apps', self._app_id,
                                        'crashes', str(crash_id)],
                             data={'format': 'text'})
        return response

    def crash_log(self, crash_id):
        """Download the crash log for a specific crash

        :param str crash_id: The specific crash to get
        :rtype: str
        :raise: ValueError

        """
        response = self._get(uri_parts=['apps', self._app_id,
                                        'crashes', str(crash_id)],
                             data={'format': 'log'})
        return response

    def crash_groups(self, version_id=None, symbolicated=False, offset=1,
                     limit=25, order='asc'):
        """List all crashes grouped by reason for an app. If version_id is
        specified, return all of the crash groupings for that version.

        :param str version_id: An optional version number to restrict groups to
        :param bool symbolicated: run crashes through the symbolication process
        :param int offset: The offset for the page of feedback
        :param int limit: The maximum number of entries per page (25, 50, 100)
        :param str order: Order of items in list, ``asc`` or ``desc``
        :rtype: Feedback

        """
        if order not in ['asc', 'desc']:
            raise ValueError('order must either be "asc" or "desc"')

        parts = ['apps', self._app_id, 'crash_reasons']
        if version_id:
            parts = ['apps', self._app_id,
                     'app_versions', str(version_id),
                     'crash_reasons']
        response = self._get(uri_parts=parts,
                             data={'symbolication': int(symbolicated),
                                   'page': offset,
                                   'per_page': limit,
                                   'order': order})
        return CrashGroups(response.get('crash_reasons', []),
                           response.get('total_entries', 0),
                           response.get('total_pages', 0),
                           response.get('current_page', 0),
                           response.get('per_page', 0))

    def crashes(self, reason_id, offset=0, limit=25):
        """Paginated list of crashes in a crash reason group.

        :param str reason_id: The id value returned for a crash group
        :param int offset: The starting offset for the crash reason
        :param int limit: The maximum number of entries returned (25, 50, 100)
        :rtype: list

        """
        response = self._get(uri_parts=['apps',
                                        self._app_id,
                                        'crash_reasons',
                                        str(reason_id)],
                             data={'page': offset,
                                   'per_page': limit})
        return Crashes(response.get('crashes', []),
                       response.get('total_entries', 0),
                       response.get('total_pages', 0),
                       response.get('current_page', 0),
                       response.get('per_page', 0))

    def delete(self):
        """Delete the app

        :rtype: bool
        :raises: ValueError

        """
        try:
            self._delete(uri_parts=['apps', self._app_id])
        except api.APIError as error:
            raise error
        self._api_id = None
        return True

    def delete_version(self, version_id, purge=False):
        """Delete a version from an application. If purge is set to True, all
        data will be removed along with the version of the application. If it
        is False, crashes and crashes will be remain.

        :param str version_id: The version id to remove
        :param bool purge: Purge all data for the version
        :rtype: bool
        :raises: ValueError

        """
        pass

    def delete_multiple_versions(self, version_id,
                                 purge=False,
                                 sort='version', number=0, keep=0,
                                 storage_percentage=None):
        """Delete multiple version from an application. If purge is set to
        True, all data will be removed along with the versions of the
        application. If it is False, crashes and crashes will be remain. To
        remove only a certain number of versions, use the number argument. To
        keep a certain number of versions, use the keep argument. If
        storage_percentage is set to an integer, any app that exceeds that
        percentage of the storage will be removed.

        sort must be either the string 'version' or 'date' and ordering of
        versions for removal is based upon this value.

        :param str version_id: The version id to remove
        :param bool purge: Purge all data for the version
        :param str sort: Either 'version' or 'date' for ordering for removal
        :param int number: Number of build versions to remove
        :param int keep: Number of build versions to keep
        :param int storage_percentage: The percentage of storage used to
                                       qualify removal
        :rtype: bool
        :raises: ValueError

        """
        pass

    def feedback(self, offset=1, limit=25, order='asc'):
        """Paginated list of feedback for an application. Returns a tuple of
        the list of feedback, total entries, total pages, current page, and
        the limit per page.

        :param int offset: The offset for the page of feedback
        :param int limit: The maximum number of entries per page (25, 50, 100)
        :param str order: Order of items in list, ``asc`` or ``desc``
        :rtype: Feedback

        """
        if order not in ['asc', 'desc']:
            raise ValueError('order must either be "asc" or "desc"')
        response = self._get(uri_parts=['apps',
                                        self._app_id,
                                        'feedback'],
                             data={'page': offset,
                                   'per_page': limit,
                                   'order': order})
        return Feedback(response.get('feedback', []),
                        response.get('total_entries', 0),
                        response.get('total_pages', 0),
                        response.get('current_page', 0),
                        response.get('per_page', 0))

    def histogram(self, start_date, end_date):
        """Get a histogram of the number of crashes between two given dates

        :param datetime.date start_date: The start date for the histogram
        :param datetime.date end_date: The end date for the histogram
        :rtype: list

        """
        response = self._get(uri_parts=['apps', self._app_id,
                                        'crashes', 'histogram'],
                             data={'start_date': start_date.isoformat(),
                                   'end_date': end_date.isoformat()})
        return dict(response.get('histogram', []))

    def post_crash(self, log_path, description=None,
                   attachment_paths=None, user_id=None, contact=None):
        """Post a crash report, e.g. if you don't want to use the HockeyApp
        SDK or develop for a custom platform.

        ..Note: The maximum allowed file size for the log file is 200kB!

        :param str log_path: Path to the log file
        :param str description: optional, file with optional information,
            e.g. excerpts from the system log
        :param list attachment_paths: A list of up to 3 files to attach to
            the crash
        :param str user_id:  optional, string with a user or device ID,
            limited to 255 chars
        :param str contact: optional, string with contact information,
            limited to 255 chars
        :rtype: bool
        :raises: ValueError

        """
        pass

    def statistics(self):
        """Get statistics about downloads, installs, and crashes for all
        versions for an application.

        :param str public_identifier: The public identifier for the application
        :rtype: list
        :raises: ValueError

        """
        return self._get(uri_parts=['apps', self._app_id,
                                    'statistics'])

    def update(self, version_id,
               notes=None, notes_type=None, notify=False, status=1,
               mandatory=None, tags=None, commit_sha=None,
               build_server_url=None, repository_url=None):
        """Update the status or metadata for an existing version.

        :param str notes: Notes for testers (optional)
        :param int notes_type: The type of formatting for the notes (0, 1)
        :param bool notify: Notify testers (optional)
        :param int status: Download status (1, 2))
        :param bool mandatory: Set version as mandatory (optional)
        :param list tags: a list of tags to apply to the version (optional)
        :param str commit_sha: The SCM commit sha for the version (optional)
        :param str build_server_url: URL of the build job (optional)
        :param str repository_url: URL to source repository (optional)
        :rtype: bool
        :raises: ValueError

        """
        pass

    def upload(self, ipa_file=None, dsym_file=None,
               notes=None, notes_type=None, notify=False, status=1,
               mandatory=None, tags=None, commit_sha=None,
               build_server_url=None, repository_url=None,
               release_type=None):
        """Upload an .ipa, .apk, or .zip file to create a new app. If an app
        with the same bundle identifier or package name and the same release
        type already exists, the uploaded file is assigned to this existing
        app.

        If the object was created without a public identifier
        ``api/2/apps/<public_identifier>/upload`` API endpoint is used.

        The ipa_file value should contain the file path of the .ipa for iOS,
        .app.zip for Mac OS X, or .apk file for Android

        :param str ipa_file: Path to a ipa file  optional (required, if dsym is
            not specified for iOS or Mac).
        :param str dsym_file: optional, file path of the .dSYM folder (iOS
            and Mac) or mapping.txt (Android)
        :param str notes: Notes for testers (optional)
        :param int notes_type: The type of formatting for the notes (0, 1)
        :param bool notify: Notify testers (optional)
        :param int status: Download status (1, 2))
        :param bool mandatory: Set version as mandatory (optional)
        :param list tags: a list of tags to apply to the version (optional)
        :param str commit_sha: The SCM commit sha for the version (optional)
        :param str build_server_url: URL of the build job (optional)
        :param str repository_url: URL to source repository (optional)
        :param int release_type: 2 for alpha, 0 for beta, 1 for live (optional)
        :return str: app_id public identifier
        :raises: ValueError

        """
        files = {}

        if ipa_file:
            if not os.path.exists(ipa_file):
                raise ValueError('File not found: %s' % ipa_file)
            ipa = open(ipa_file, 'rb')
            ipa_file_name = os.path.split(ipa_file)[1]
            files["ipa"] = (ipa_file_name, ipa)

        if dsym_file:
            if not os.path.exists(dsym_file):
                raise ValueError('File not found: %s' % dsym_file)
            dsym_file_name = os.path.split(dsym_file)[1]
            if "dSYM" in dsym_file and os.path.isdir(dsym_file):
                dsym_zip = tempfile.NamedTemporaryFile(delete=False)
                z = zipfile.ZipFile(dsym_zip, 'w')
                rootlen = len(os.path.split(dsym_file)[0]) + 1
                for base, dirs, list_files in os.walk(dsym_file):
                    for f in list_files:
                        fn = os.path.join(base, f)
                        z.write(fn, fn[rootlen:])
                z.close()
                dsym_zip.seek(0)
                files["dsym"] = (dsym_file_name + '.zip', dsym_zip)
            else:
                files["dsym"] = (dsym_file_name, dsym_file)

        data = {}

        validation_map = {
            "notes": (notes, str, None),
            "notes_type": (notes_type, int, [0, 1]),
            "notify": (notify, int, [0, 1]),
            "status": (status, int, [1, 2]),
            "mandatory": (mandatory, int, [0, 1]),
            "tags": (tags, list, None),
            "commit_sha": (commit_sha, str, None),
            "build_server_url": (build_server_url, str, None),
            "repository_url": (repository_url, str, None),
            "release_type": (release_type, int, [0, 1, 2]),
        }

        for key in validation_map:
            val, t, valids = validation_map[key]
            if val:
                if type(val) is not t:
                    ValueError('Invalid type for `%s`' % key)
                if valids and val not in valids:
                    ValueError('Invalid value for `%s`' % key)
                data[key] = val

        try:
            response = self._post(uri_parts=['apps', 'upload'],
                                  data=data,
                                  files=files)
        except api.APIError as error:
            raise error

        self._app_id = response['public_identifier']
        return response['public_identifier']

    def update_crash_reason(self, reason_id, status=None, ticket_url=None):
        """Update a crash reason grouping with an optional status flag and
        optional ticket URL.

        Status constants:

          - Application.CRASH_STATUS_OPEN (0)
          - Application.CRASH_STATUS_RESOLVED (1)
          - Application.CRASH_STATUS_IGNORED (2)

        :param str reason_id: The crash group id
        :param int status: Crash group status (0, 1, 2))
        :param str ticket_url: URL a ticket for this crash reason group
        :rtype: bool
        :raises: ValueError

        """
        data = dict()
        if status:
            if status not in [self.CRASH_STATUS_OPEN,
                              self.CRASH_STATUS_RESOLVED,
                              self.CRASH_STATUS_IGNORED]:
                raise ValueError('Invalid status value')
            data['status'] = status
        if ticket_url:
            data['ticket_url'] = ticket_url
        try:
            self._post(uri_parts=['apps', self._app_id,
                                  'crash_reasons', str(reason_id)],
                       data=data)
        except api.APIError as error:
            raise error
        return True

    def versions(self):
        """Get statistics about downloads, installs, and crashes for all
        versions for an application.

        :rtype: list
        :raises: ValueError

        """
        return self._get(uri_parts=['apps',
                                    self._app_id,
                                    'app_versions'])['app_versions']

    def _check_app_id(self, value):
        """Check the public identifier value passed in and ensure it's the
        proper type of value.

        :param str value: The public identifier for the application
        :raises: ValueError

        """
        if isinstance(value, int) or value.isdigit():
            raise ValueError('Must pass in the public_identifier value, '
                             'not the numeric app id value')
        if not self.APP_ID_PATTERN.match(value):
            raise ValueError('public_identifier is a 32 character hex digest '
                             'hash value')


# Deprecated classes for transitional support, to be removed in future versions

class AppList(Applications):
    """Return the application list for a given token"""

    def __init__(self, token):
        warnings.warn('Deprecated for hockeyapp.Applications',
                      DeprecationWarning)
        super(AppList, self).__init__(token)

    def execute(self):
        self.list()
