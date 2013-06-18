"""
cli.py

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2011-09-12'

import logging
import optparse
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

def parse_options():
    """Parse commandline options.

    :returns: Tuple of OptionParser object, options and arguments
    """
    usage = "usage: %prog -k <api_key> [options [-i app_id] [-d crash_id]]"
    version_string = "%%prog %s" % __version__
    description = "Hockeyapp API Client"

    # Create our parser and setup our command line options
    parser = optparse.OptionParser(usage=usage,
                                   version=version_string,
                                   description=description)

    parser.add_option("-k", "--api-key",
                      action="store", dest="api_key",
                      help="Supply the API Token from hockeyapp.net")

    parser.add_option("-a", "--list-applications",
                      action="store_true", dest="list_applications",
                      help="List the applications available at HockeyApp")

    parser.add_option("-u", "--list-users",
                      action="store_true", dest="list_users",
                      help="List users associated with the specified HockeyApp")

    parser.add_option("-c", "--list-crashes",
                      action="store_true", dest="list_crashes",
                      help="List crashes associated with the specified HockeyApp")

    parser.add_option("--add-app-user",
                      action="store_true", dest="add_app_user",
                      help="Add a user to a HockeyApp")

    parser.add_option("-o", "--offset",
                      action="store", dest="offset", default=1,
                      help="Use an offset for the crash list")

    parser.add_option("-i", "--app-id",
                      action="store", dest="app_id",
                      help="The application identifier at HockeyApp")

    parser.add_option("-d", "--detail",
                      action="store", dest="detail",
                      help="Get the detail for a crash ID at HockeyApp")

    parser.add_option("-e", "--email",
                      action="store", dest="email",
                      help="User email address")

    parser.add_option("-m", "--mode",
                      action="store", dest="mode", default="text",
                      help="Set the mode for retreiving the detail " + 
                           "for a crash [log, text]")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Turn on debug mode")

    options, arguments = parser.parse_args()
    return parser, options, arguments


def main():
    """Main commandline invocation function."""
    # Parse our options and arguments
    parser, options, args = parse_options()

    # If debugging is turned on, turn on logging and set the level
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Make sure we have an api key
    if not options.api_key:
        sys.stderr.write('\nERROR: Missing API Key\n\n')
        parser.print_help()
        sys.exit(1)

    if options.list_applications:
        app_list = apps.AppList(options.api_key)
        try:
            print app_list.execute()
        except APIError as e:
            print_api_error(e)

        return

    if options.list_users:
        if not options.app_id:
            sys.stderr.write('\nERROR: Missing App ID\n\n')
            parser.print_help()
            sys.exit(1)

        user_list = team.AppUsers(options.api_key, options.app_id)
        try:
            print user_list.execute()
        except APIError as e:
            print_api_error(e)

        return

    if options.add_app_user:
        if not options.app_id:
            sys.stderr.write('\nERROR: Missing App ID\n\n')
            parser.print_help()
            sys.exit(1)

        if not options.email:
            sys.stderr.write('\nERROR: Missing Email Address\n\n')
            parser.print_help()
            sys.exit(1)

        add_user = team.AppAddUser(options.api_key, options.app_id, options.email)
        try:
            print add_user.execute()
        except APIError as e:
            print_api_error(e)

        return

    if options.list_crashes:
        crash_list = crashes.CrashList(options.api_key, options.app_id, options.offset)
        try:
            print crash_list.execute()
        except APIError as e:
           print_api_error(e)

        return

    if options.detail:
        crash_detail = crashlog.CrashLog(options.api_key,
                                         options.app_id,
                                         options.detail,
                                         options.mode)
        try:
            print crash_detail.execute()
        except APIError as e:
            sys.stderr.write("\nERROR: %s\n\n" % str(e))

        return

    sys.stderr.write('\nERROR: You must select an action to take\n\n')
    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
    main()
