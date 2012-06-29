"""
A module to build the connections.

* Each expects only a parameters named tuple on initiation.

* Each has a connection parameter
"""
#python
from types import StringType

from tottest.connections import adbconnection
from tottest.baseclass import BaseClass
from tottest.connections import sshconnection
from tottest.commons import errors


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
        self.parameters = parameters
        self._hostname = None
        self._username = None
        self.password = parameters.password
        self._connection = None
        return

    @property
    def hostname(self):
        """
        :rtype: StringType
        :return: The hostname (I.P.) to connect to
        :raise: ConfigurationError if not set
        """
        if self._hostname is None:
            self._hostname = self.get_required("hostname")
        return self._hostname

    @property
    def username(self):
        """
        :rtype: StringType
        :return: user login name
        :raise: ConfigurationError if not found
        """
        if self._username is None:
            self._username = self.get_required("username")
        return self._username
    
    @property
    def connection(self):
        if self._connection is None:
            self.logger.debug("Creating the ssh connection.")
            self._connection = sshconnection.SSHConnection(hostname=self.hostname,
                                                           username=self.username,
                                                           password=self.password)
        return self._connection

    def get_required(self, parameter):
        """
        :param:

         - `parameter`: the name of parameter to get
        """
        param = getattr(self.parameters, parameter)
        if type(param) is not StringType:
            raise errors.ConfigurationError("`{0}` is a required option for section `{1}` (got '{2}')".format(parameter, self.parameters.section, param))
        return param
# end class SshConnectionBuilder
