"""
A module to query the device for interface information.
"""
#python libraries
import re

from tottest.baseclass import BaseClass
from tottest.commons import enumerations
from tottest.commons import expressions
from tottest.commons import errors

CommandError = errors.CommandError


class WpaCliCommand(BaseClass):
    """
    The WpaCliCommand interprets ifconfig
    """
    def __init__(self, connection, interface=None, operating_system=None):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface to check
         - `operating_system` : The operating system on the devices.
        """
        super(WpaCliCommand, self).__init__()
        self.connection = connection
        self._interface = interface
        self._operating_system = operating_system
        self._ip_address = None
        self._mac_address = None
        self._status = None
        self._ssid = None
        self.status_command = "status"
        self.interface_list_command = "interface_list"
        return

    @property
    def operating_system(self):
        """
        :return: the operating system for the device to query
        """
        if self._operating_system is None:
            self._operating_system = enumerations.OperatingSystem.linux
        return self._operating_system

    @property
    def status(self):
        """
        This is dynamically generated.
        
        :return: The status of the wpa-connection
        """
        return ''.join([line for line in self.connection.wpa_cli(self.status_command)[0]])

    
    @property
    def ip_address(self):
        """
        This is dynamically generated.
        
        :return: The IP Address of the interface
        """
        expression = expressions.WPA_IP
        name = expressions.IP_ADDRESS_NAME
        command = self.status_command
        return self._match(expression,
                           name,
                           command)

    @property
    def ssid(self):
        """
        This is dynamically generated.
        
        :return: The SSID of the attached AP
        """
        expression = expressions.WPA_SSID
        name = expressions.SSID_NAME
        command = self.status_command
        return self._match(expression, name, command)
    
    @property
    def interface(self):
        """
        This is found once and stored.
        
        :return: The connected interface
        """
        if self._interface is None:
            expression = expressions.WPA_INTERFACE
            name = expressions.INTERFACE_NAME
            command = self.interface_list_command
            self._interface = self._match(expression,
                                          name,
                                          command)
        return self._interface
    
    @property
    def mac_address(self):
        """
        This is found once and stored.
        
        :return: MAC Address of the interface
        """
        if self._mac_address is None:
            expression = expressions.WPA_MAC
            name = expressions.MAC_ADDRESS_NAME
            command = self.status_command
            self._mac_address = self._match(expression,
                                            name,
                                            command)
        return self._mac_address

    
    def _match(self, expression, name, arguments):
        """
        :param:

         - `expression`: The regular expression to match
         - `name`: The group name to pull the match out of the line
         - `command`: The arguments to give to the wpa_cli
         
        :return: The named-group that matched or None
        """
        expression = re.compile(expression)
        output, error = self.connection.wpa_cli(arguments)
        for line in output:
            match = expression.search(line)
            if match:
                return match.group(name)
        err = error.read()
        if len(err):
            self.logger.error(err)
            raise CommandError(err)
        return
# end class WpaCliCommand
    
if __name__ == "__main__":
    from tottest.connections import adbconnection
    connection = adbconnection.ADBShellConnection()
    command = WpaCliCommand(connection)
    print command.mac_address
    print command.ip_address
    print command.interface
    print command.status
    print command.ssid
