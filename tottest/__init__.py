"""
The time-to-recover-test (TTR) characterizes the recovery time for a device.

Here the recovery time is measured from the time the WiFi is enabled until the device is able to ping a target a certain amount of times.

Since pings are used, if the device doesn't have a static IP address, the time will include DHCP request times, which varies depending on the Access Point used.

Although the time reported includes this, the test includes the ability to capture logs which in many cases will allow you to determine the time for association to the Access Point as well (which appears to be much more consistent than DHCP request responses).

Although it is available as a library, the test is intended to be used as a command-line command called `ttr`. It has four main sub-commands - `run`, `fetch`, help`, `test`. A typical use-case would be to fetch the setup files::

    tty fetch

This will copy a set of files to the current working directory and allow you to edit `ttr.ini`, the default file used by the `ttr` command.

The `fetch` will also copy a file called `source_this_for_sl4a` which you can source to start the `sl4a` server and forward the ports (assuming that the ADB server is running)::

    source source_this_for_sl4a

Once this is done and the `ttr.ini` file is edited to match the current configuration, you run the test by entering::

    ttr run

The `run` will by default look for any file that ends with `.ini` in it as the configuration file. If it finds more than one it will assume you want to run multiple tests and execute them all so if you have multiple files and only want to run one or a subset with a specific wildcard match, pass that in as an option::

    ttr run [filename | file-glob]
"""
from connections.localconnection import LocalNixConnection
