"""
cli.py

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2011-09-12'

import logging
import argparse
import sys

from . import __version__
from .api import APIError
from . import apps
from . import crashes
from . import crashlog
from . import team


def print_api_error(e):
    """ Print an APIError exception to stderr

    :param e: The exception
    :type e: APIError

    """
    sys.stderr.write("\nERROR: %s\n" % str(e))


def parse_args():
    """Parse commandline arguments.

    :returns: Tuple of OptionParser object and arguments
    """
    version_string = "%%(prog)s %s" % __version__
    description = "Hockeyapp API Client"

    # Create our parser and setup our command line args
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-V", "--version", action='version',
                        version=version_string)
    parser.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="turn on debug mode")

    parser.add_argument("-k", "--api-key",
            dest="api_key", required=True,
            help="Supply the API Token from hockeyapp.net")

    # Define subcommands
    subparsers = parser.add_subparsers(title="commands", metavar="COMMAND",
            description="See '%(prog)s COMMAND -h' for more information on a specific command.")

    def show(request):
        print request.execute()

    la = subparsers.add_parser('list-applications',
            help="List the applications available at HockeyApp")
    la.set_defaults(func=lambda a:
            show(apps.AppList(a.api_key)))

    lu = subparsers.add_parser('list-users',
            help="List users associated with the specified HockeyApp")
    lu.set_defaults(func=lambda a:
            show(team.AppUsers(a.api_key, a.app_id)))

    lc = subparsers.add_parser('list-crashes',
            help="List crashes associated with the specified HockeyApp")
    lc.set_defaults(func=lambda a:
            show(crashes.CrashList(a.api_key, a.app_id, a.offset)))

    aau = subparsers.add_parser("add-app-user",
            help="Add a user to a HockeyApp")
    aau.set_defaults(func=lambda a:
            show(team.AppAddUser(a.api_key, a.app_id, a.email)))

    d = subparsers.add_parser("detail",
            help="Get the detail for a crash ID at HockeyApp")
    d.set_defaults(func=lambda a:
            show(crashlog.CrashLog(a.api_key, a.app_id, a.crash_id, a.mode)))

    # Arguments common for many actions
    for p in (lu, lc, aau, d):
        p.add_argument("app_id",
                       help="The application identifier at HockeyApp")

    # Command specific arguments
    lc.add_argument("-o", "--offset",
            default=1,
            help="Use an offset for the crash list")

    aau.add_argument("email",
            help="User email address")

    d.add_argument("crash_id",
            help="The crash ID")
    d.add_argument("-m", "--mode",
            default="text", choices=['log', 'text'],
            help="Set the mode for retreiving the detail for a crash")

    # Print help message when there's no subcommand
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    arguments = parser.parse_args()
    return parser, arguments


def main():
    """Main commandline invocation function."""
    # Parse our and arguments
    parser, args = parse_args()

    # If debugging is turned on, turn on logging and set the level
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    try:
        args.func(args)
    except APIError as e:
        print_api_error(e)


if __name__ == '__main__':
    main()
