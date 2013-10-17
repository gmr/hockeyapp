HockeyApp Python Client
=======================
API and command-line client for managing applications, users, and crashes at HockeyApp.

|PyPI version| |Downloads| |Build Status|

Python Versions: 2.6, 2.7, 3.2, 3.3

CLI Usage
---------

        ./hockeyapp-cli

        usage: hockeyapp-cli [-h] [-V] [-v] -k API_KEY COMMAND ...

        Hockeyapp API Client

        optional arguments:
          -h, --help            show this help message and exit
          -V, --version         show program's version number and exit
          -v, --verbose         turn on debug mode
          -k API_KEY, --api-key API_KEY
                                Supply the API Token from hockeyapp.net

        commands:
          See 'hockeyapp-cli COMMAND -h' for more information on a specific command.

          COMMAND
            list-applications   List the applications available at HockeyApp
            list-users          List users associated with the specified HockeyApp
            list-crashes        List crashes associated with the specified HockeyApp
            add-app-user        Add a user to a HockeyApp
            detail              Get the detail for a crash ID at HockeyApp
            list-versions       List the versions of an app
            version-delete      Delete a specified version
            version-add         Add a new version of an app

Example usage
-------------

        import hockeyapp

        token = 'abcdef0123456789abcdef0123456789'             # The HockeyApp API Auth Token
        public_identifier = '0123456789abcdef0123456789abcdef' # The public identifier app id

        apps = hockeyapp.Applications(token)
        print apps.list()

        app = hockeyapp.Application(token, public_identifier)
        print app.statistics()
        print app.versions()


.. |PyPI version| image:: https://badge.fury.io/py/hockeyapp.png
   :target: http://badge.fury.io/py/hockeyapp
.. |Downloads| image:: https://pypip.in/d/hockeyapp/badge.png
   :target: https://crate.io/packages/hockeyapp
.. |Build Status| image:: https://travis-ci.org/gmr/hockeyapp.png?branch=master
   :target: https://travis-ci.org/gmr/hockeyapp
