"""
Command Line app for interacting with HockeyApp API

"""
import argparse
import logging
import sys

from hockeyapp import __version__
from hockeyapp import api
from hockeyapp import app
from hockeyapp import crashes
from hockeyapp import crashlog
from hockeyapp import team
from hockeyapp import version


def print_api_error(error):
    """ Print an APIError exception to stderr

    :param hockapp.api.APIError error: The exception

    """
    sys.stderr.write('\nERROR: %s\n' % error)


def parse_args():
    """Parse commandline arguments.

    :rtype: tuple(argparse.ArgumentParser, argparse.Namespace)

    """
    version_string = '%%(prog)s %s' % __version__
    description = 'Hockeyapp API Client'

    # Create our parser and setup our command line args
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-V', '--version', action='version',
                        version=version_string)
    parser.add_argument('-v', '--verbose',
                        action='store_true', dest='verbose',
                        help='turn on debug mode')

    parser.add_argument('-k', '--api-key',
                        dest='api_key', required=True,
                        help='Supply the API Token from hockeyapp.net')

    # Define subcommands
    subparsers = parser.add_subparsers(title='commands', metavar='COMMAND',
                                       description='See "%(prog)s COMMAND -h" '
                                                   'for more information on a '
                                                   'specific command.')

    def show(request):
        print(request.execute())

    la = subparsers.add_parser('list-applications',
                               help='List the applications available')
    la.set_defaults(func=lambda a:
                    show(apps.AppList(a.api_key)))

    lu = subparsers.add_parser('list-users',
                               help='List users associated with the '
                                    'specified HockeyApp')
    lu.set_defaults(func=lambda a:
                    show(team.AppUsers(a.api_key, a.app_id)))

    lc = subparsers.add_parser('list-crashes',
                               help='List crashes associated with the '
                                    'specified HockeyApp')
    lc.set_defaults(func=lambda a:
                    show(crashes.CrashList(a.api_key, a.app_id, a.offset)))

    aau = subparsers.add_parser('add-app-user',
                                help='Add a user to a HockeyApp')
    aau.set_defaults(func=lambda a:
                     show(team.AppAddUser(a.api_key, a.app_id, a.email)))

    d = subparsers.add_parser('detail',
                              help='Get the detail for a crash ID')
    d.set_defaults(func=lambda a:
                   show(crashlog.CrashLog(a.api_key, a.app_id,
                                          a.crash_id, a.mode)))

    lv = subparsers.add_parser('list-versions',
                               help='List the versions of an app')
    lv.set_defaults(func=lambda options:
                    show(version.AppVersions(options.api_key, options.app_id)))

    vd = subparsers.add_parser('version-delete',
                               help='Delete a specified version')
    vd.set_defaults(func=lambda a:
                    show(version.AppVersionDelete(a.api_key, a.app_id,
                                                  a.version_id, a.purge)))

    va = subparsers.add_parser('version-add',
                               help='Add a new version of an app')
    types = dict(textile=0, markdown=1)
    va.set_defaults(func=lambda a:
                    show(version.AppVersionAdd(a.api_key,
                                               a.app_id,
                                               a.ipa,
                                               a.dsym,
                                               a.notes.read(),
                                               types[a.notes_type],
                                               not a.nonotify,
                                               not a.notdownloadable,
                                               a.tags)))

    # Arguments common for many actions
    for p in (lu, lc, aau, d, lv, vd, va):
        p.add_argument('app_id',
                       help='The application identifier at HockeyApp')

    # Command specific arguments
    lc.add_argument('-o', '--offset',
                    default=1,
                    help='Use an offset for the crash list')

    aau.add_argument('email',
                     help='User email address')

    d.add_argument('crash_id',
                   help='The crash ID')
    d.add_argument('-m', '--mode',
                   default='text', choices=['log', 'text'],
                   help='Set the mode for retreiving the detail for a crash')

    vd.add_argument('version_id',
                    help='The version ID')
    vd.add_argument('-p', '--purge',
                    action='store_true',
                    help='Remove permanentely')

    va.add_argument('ipa', type=argparse.FileType('r'),
                    help='The ipa or apk to upload')
    va.add_argument('--dsym', type=argparse.FileType('r'),
                    help='The .dSYMzip or mapping.txt file')
    va.add_argument('notes', type=argparse.FileType('r'),
                    help='A file containing the release notes')
    va.add_argument('--notes_type',
                    default='markdown', choices=types,
                    help='How to parse the release notes')
    va.add_argument('--nonotify',
                    action='store_true',
                    help='Do not notify tester')
    va.add_argument('--notdownloadable',
                    action='store_true',
                    help='Do not allow downloads')
    va.add_argument('--tags',
                    help='Restrict download to a comma separated list of tags')

    # Print help message when there's no subcommand
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser, parser.parse_args()


def main():
    """Main commandline invocation function."""
    parser, args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    try:
        args.func(args)
    except api.APIError as error:
        print_api_error(error)


if __name__ == '__main__':
    main()
