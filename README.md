HockeyApp.net Python Client
===========================

Access your crash log and crash detail data for iOS applications tracked at
hockeyapp.net.

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

Example usage
-------------

        import hockeyapp

        api_key = 'Your API Key'
        app_id = 'App ID to Query'
        crash_id = 1234

        app_list = hockeyapp.apps.AppList(api_key)
        print app_list.execute()
        return

        crash_list = hockeyapp.crashes.CrashList(api_key, app_id)
        print crash_list.execute()
        return


        crash_detail = hockeyapp.crashlog.CrashLog(api_key, app_id, crash_id)
        print crash_detail.execute()
        return

Author
------
Gavin M. Roy <gmr@myyearbook.com>

Copyright and License
---------------------
Copyright (c) 2011, Insider Guides, Inc. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of Insider Guides, Inc., its website properties nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
