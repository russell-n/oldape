"""
A module to query the device for interface information.
"""
#python libraries
import re

from apetools.baseclass import BaseClass
from apetools.commons import enumerations
from apetools.commons import expressions
from apetools.commons import errors

MAC_UNAVAILABLE = "MAC Unavailable (use `netcfg`)"
CommandError = errors.CommandError


class IwCommand(BaseClass):
    """
    The IwCommand interprets iw
    """
    def __init__(self, connection, interface=None, operating_system=None):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface to check
         - `operating_system` : The operating system on the devices.
        """
        super(IwCommand, self).__init__()
        self.connection = connection
        self._interface = interface
        self._operating_system = operating_system
        self._rssi = None
        self._mac_address = None
        self._ssid = None
        self.bssid = ""
        self._channel = None
        self.noise = 'NA'
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
    def interface(self):
        """
        :return: the name of the wireless interface
        """
        if self._interface is None:
            expression = expressions.IW_INTERFACE
            name = expressions.INTERFACE_NAME
            command = "dev"
            self._interface = self._match(expression, name, command)
        return self._interface

    @property
    def ssid(self):
        """
        The ssid of the attached ap
        """
        self.logger.debug('Getting the SSID')
        name = 'SSID'

        expr = expressions.NAMED.format(name=name,
                                        pattern=expressions.EVERYTHING)
        expression = 'SSID:' + expressions.SPACES + expr + '$'
        command = '{i} link'.format(i=self.interface)
        return self._match(expression, name, command)
    
    @property
    def channel(self):
        """
        The channel of the attached ap (actually frequency right now)
        """
        self.logger.debug('Getting the channel')
        name = 'channel'

        expr = expressions.NAMED.format(name=name,
                                        pattern=expressions.INTEGER)
        expression = 'freq:' + expressions.SPACES + expr
        command = '{i} link'.format(i=self.interface)
        return self._match(expression, name, command)
    
    @property
    def rssi(self):
        """
        This is dynamically generated
        
        :return: The rssi for the interface
        """        
        expression = expressions.IW_RSSI
        name = expressions.RSSI_NAME
        command = "dev {i} link".format(i=self.interface)
        return self._match(expression, name, command)
    
    @property
    def mac_address(self):
        """
        :return: MAC Address of the interface
        """
        if self._mac_address is None:
            expression = expressions.MAC_ADDRESS
            name = expressions.MAC_ADDRESS_NAME
            command = "{i} link".format(i=self.expression)
            self._mac_address = self._match(expression, name, command)
        return self._mac_address
    
    def _match(self, expression, name, command):
        """
        :param:

         - `expression`: The regular expression to match
         - `name`: The group name to pull the match out of the line
         - `command`: The command to send to iw
         
        :return: The named-group that matched or None
        """
        expression = re.compile(expression)
        with self.connection.lock:
            output, error = self.connection.iw(command)
        for line in output:
            match = expression.search(line)
            if match:
                return match.group(name)
        err = error.read()
        if len(err):
            self.logger.error(err)
            if "No such device" in err:
                raise CommandError("Unknown Interface: {0}".format(self.interface))
            else:
                raise CommandError(err)
        return ''

    def __str__(self):
        return "({iface}) RSSI: {rssi}".format(iface=self.interface,
                                               rssi=self.rssi)
# end class IfconfigCommand
    
if __name__ == "__main__":
    from apetools.connections import adbconnection
    connection = adbconnection.ADBShellConnection()
    iw = IwCommand(connection)
    print str(iw)
