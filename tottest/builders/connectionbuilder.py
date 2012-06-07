"""
A module to build the connections.

* Each expects only a parameters named tuple on initiation.

* Each has a connection parameter
"""

from tottest.connections import adbconnection
from tottest.baseclass import BaseClass
from tottest.connections import sshconnection

class AdbShellConnectionBuilder(BaseClass):
    """
    Use this to get an adb shell connection
    """
    def __init__(self, parameters=None):
        """
        :param:

         - `parameters`: Not used, just here to keep the interface unifomr
        """
        super(AdbShellConnectionBuilder, self).__init__()
        self._connection = None
        return

    @property
    def connection(self):
        """
        :rtype: ADBShellConnection
        :return: A built ADB shell connection
        """
        if self._connection is None:
            self.logger.debug("Creating the adb shell connection")
            self._connection = adbconnection.ADBShellConnection()
        return self._connection
# end class AdbShellConnectionBuilder

class SshConnectionBuilder(BaseClass):
    """
    Use this to get an ssh connection
    """
    def __init__(self, parameters):
        """
        :param:

         - `parameters`: An object with `hostname`, `username`, and `password` attributes
        """
        super(SshConnectionBuilder, self).__init__()
        self.hostname = parameters.hostname        
        self.username = parameters.username
        self.password = parameters.password
        self._connection = None
        return

    @property
    def connection(self):
        if self._connection is None:
            self.logger.debug("Creating the ssh connection.")
            self._connection = sshconnection.SSHConnection(hostname=self.hostname,
                                                           username=self.username,
                                                           password=self.password)
        return self._connection
# end class SshConnectionBuilder
