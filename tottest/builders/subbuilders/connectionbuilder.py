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

         - `parameters`: Not used, just here to keep the interface uniform
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

class SSHConnectionBuilder(BaseClass):
    """
    Use this to get an ssh connection
    """
    def __init__(self, parameters):
        """
        :param:

         - `parameters`: An object with `hostname`, `username`, and `password` attributes
        """
        super(SSHConnectionBuilder, self).__init__()
        self.parameters = parameters
        self._hostname = None
        self._username = None
        self._password = None
        self._connection = None
        self._operating_system = None
        return

    @property
    def operating_system(self):
        """
        :return: parameters.operating_system
        """
        if self._operating_system is None:
            try:
                self._operating_system = self.parameters.operating_system
            except AttributeError as error:
                self.logger.debug(error)
                self.logger.warning("Operating System not found in: {0}".format(self.parameters))
        return self._operating_system

    @property
    def hostname(self):
        """
        :rtype: StringType
        :return: The hostname (I.P.) to connect to
        :raise: ConfigurationError if not set
        """
        if self._hostname is None:
            try:
                self._hostname = self.parameters.hostname
            except AttributeError as error:
                self.logger.debug(error)
                try:
                    self._hostname = self.parameters.address
                except AttributeError as error:
                    self.logger.debug(error)
                    raise errors.ConfigurationError("`hostname` is a required parameter for the SSHConnection")
        return self._hostname

    @property
    def username(self):
        """
        :rtype: StringType
        :return: user login name
        :raise: ConfigurationError if not found
        """
        if self._username is None:
            try:
                self._username = self.parameters.username
            except AttributeError as error:
                self.logger.debug(error)
                try:
                    self._username = self.parameters.login
                except AttributeError as error:
                    self.logger.debug(error)
                    raise errors.ConfigurationError("`username` is a required parameter for the SSHConnection")                
        return self._username

    @property
    def password(self):
        """
        :return: the password for the connection (sets to None if not given in the parameters)
        """
        if self._password is None:
            try:
                self._password = self.parameters.password
            except AttributeError as error:
                self.logger.debug(error)
                self._password = None
        return self._password
    
    @property
    def connection(self):
        if self._connection is None:
            self.logger.debug("Creating the ssh connection.")
            self._connection = sshconnection.SSHConnection(hostname=self.hostname,
                                                           username=self.username,
                                                           password=self.password,
                                                           operating_system=self.operating_system)
        return self._connection
# end class SshConnectionBuilder

class ConnectionBuilderTypes(object):
    __slots__ = ()
    ssh = 'ssh'
# end class BuilderTypes

connection_builders = {ConnectionBuilderTypes.ssh: SSHConnectionBuilder}
