"""
A module to query the device for interface information.
"""
#python libraries
import re
from itertools import tee

from tottest.baseclass import BaseClass
from tottest.commons import enumerations
from tottest.commons import expressions

MAC_UNAVAILABLE = "MAC Unavailable (use `netcfg`)"


class IfconfigCommand(BaseClass):
    """
    The IfconfigCommand interprets ifconfig
    """
    def __init__(self, connection, interface, operating_system=None):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface to check
         - `operating_system` : The operating system on the devices.
        """
        super(IfconfigCommand, self).__init__()
        self.connection = connection
        self.interface = interface
        self._operating_system = operating_system
        self._ip_address = None
        self._mac_address = None
        self._output = None
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
    def ip_address(self):
        """
        :return: The IP Address of the interface
        """
        if self._ip_address is None:
            if self.operating_system == enumerations.OperatingSystem.linux:
                expression = expressions.LINUX_IP
            elif self.operating_system == enumerations.OperatingSystem.android:
                expression = expressions.ANDROID_IP
            self._ip_address = self._match(expression,
                                           expressions.IP_ADDRESS_NAME)
        return self._ip_address

    @property
    def mac_address(self):
        """
        :return: MAC Address of the interface
        """
        if self._mac_address is None:
            if self.operating_system == enumerations.OperatingSystem.linux:
                expression = expressions.LINUX_MAC
            elif self.operating_system == enumerations.OperatingSystem.android:
                self._mac_address =  MAC_UNAVAILABLE
                return self._mac_address
            self._mac_address = self._match(expression,
                                            expressions.MAC_ADDRESS_NAME)
        return self._mac_address
    
    @property
    def output(self):
        """
        This stores the value so it won't reflect updated changes.
        Does a tee so that it can be used by more than one attribute
                
        :return: The output of the ifconfig command on the device
        """
        if self._output is None:
            self._output, output = tee(self.connection.ifconfig(self.interface))
        else:
            self._output, output = tee(self._output)
        return output

    def _match(self, expression, name):
        """
        :param:

         - `expression`: The regular expression to match
         - `name`: The group name to pull the match out of the line
         
        :return: The named-group that matched or None
        """
        expression = re.compile(expression)
        for line in self.output:
            match = expression.search(line)
            if match:
                return match.group(name)
        return
# end class IfconfigCommand
    