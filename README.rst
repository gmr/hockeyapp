HockeyApp.net Python Client
===========================
Access your crash log and crash detail data for iOS, Mac OSX, and Android
applications tracked at hockeyapp.net.

|PyPI version| |Downloads| |Build Status|

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

        token = 'Your API Key'
        public_identifier = 'Public identifier value for the app'
        crash_id = 1234

        app = hockeyapp.Application(token)
        print app.list()
        print app.statistics(public_identifier)


.. |PyPI version| image:: https://badge.fury.io/py/hockeyapp.png
   :target: http://badge.fury.io/py/hockeyapp
.. |Downloads| image:: https://pypip.in/d/hockeyapp/badge.png
   :target: https://crate.io/packages/hockeyapp
.. |Build Status| image:: https://travis-ci.org/gmr/hockeyapp.png?branch=master
   :target: https://travis-ci.org/gmr/hockeyapp
