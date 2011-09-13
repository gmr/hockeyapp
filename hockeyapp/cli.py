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
from . import apps
from . import crashes
from . import crashlog

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
                      help="Run in the foreground in debug mode.")

    parser.add_option("-a", "--list-applications",
                      action="store_true", dest="list_applications",
                      help="List the applications available at HockeyApp")

    parser.add_option("-c", "--list-crashes",
                      action="store_true", dest="list_crashes",
                      help="List the applications available at HockeyApp")

    parser.add_option("-i", "--app-id",
                      action="store", dest="app_id",
                      help="The application identifier at HockeyApp")

    parser.add_option("-d", "--detail",
                      action="store", dest="detail",
                      help="Get the detail for a crash ID at HockeyApp")

    parser.add_option("-o", "--offset",
                      action="store", dest="offset", default=1,
                      help="Use an offset for the crash list")

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
        print app_list.execute()
        return

    if options.list_crashes:
        crash_list = crashes.CrashList(options.api_key, options.app_id)
        print crash_list.execute()
        return

    if options.detail:
        crash_detail = crashlog.CrashLog(options.api_key,
                                         options.app_id,
                                         options.detail)
        print crash_detail.execute()
        return

    sys.stderr.write('\nERROR: You must select an action to take\n\n')
    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
    main()
