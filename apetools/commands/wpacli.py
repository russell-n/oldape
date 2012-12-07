"""
A module to query the device for interface information.
"""
#python libraries
import re

from apetools.baseclass import BaseClass
from apetools.commons import enumerations
from apetools.commons import expressions
from apetools.commons import errors

CommandError = errors.CommandError


class WpaCliCommand(BaseClass):
    """
    The WpaCliCommand interprets ifconfig
    """
    def __init__(self, connection, interface=None):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface to check
        """
        super(WpaCliCommand, self).__init__()
        self.connection = connection
        self._interface = interface
        self._ip_address = None
        self._mac_address = None
        self._status = None
        self._ssid = None
        self._supplicant_state = None
        self.status_command = "status"
        self.interface_list_command = "interface_list"
        return


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
    def supplicant_state(self):
        """
        This is dynamically generated.

        :return: The supplicant-state
        """
        expression = expressions.WPA_SUPPLICANT_STATE
        name = expressions.SUPPLICANT_STATE_NAME
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

    def __str__(self):
        return "({i}) IP: {ip}, MAC: {mac}, ssid: {ssid}, suplicant-state: {sup}".format(i=self.interface,
                                                                                         ip = self.ip_address,
                                                                                         mac = self.mac_address,
                                                                                         ssid = self.ssid,
                                                                                         sup=self.supplicant_state)

# end class WpaCliCommand
    
if __name__ == "__main__":
    from apetools.connections import adbconnection
    connection = adbconnection.ADBShellConnection()
    command = WpaCliCommand(connection)
    print str(command)
    print command.status
