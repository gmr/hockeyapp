Command Line Usage
==================

::
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
