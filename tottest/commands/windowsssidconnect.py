"""
A re-associator between a device and a SSID/profile
"""

from tottest.baseclass import BaseClass
from tottest.commons.errors import CommandError

class WindowsSSIDConnect(BaseClass):
    """
    A class to associate a windows device with a known wifi profile
    """
    def __init__(self, connection):
        super(WindowsSSIDConnect, self).__init__()
        self.connection = connection
        return

    def validate(self, output):
        """
        :param:

         - `output`: iterator over output from the netsh connect command
        """
        for line in output:
            self.logger.debug(line)
            if line.startswith("There is no profile ") or line.startswith("There is no wireless interface"):
                raise CommandError(line)
            if line.startswith("Connection request was completed successfully."):
                self.logger.info(line)
                break
        return

    def __call__(self, ssid):
        """
        :param:

         - `ssid`: name of the SSID/profile on the device to pass to netsh

        :raise: CommandError if an output error is found.
        """
        output, error = self.connection.netsh('wlan connect name="{0}" ssid="{0}"'.format(ssid))
        self.validate(output)
        return
# end class WindowsSSIDConnect