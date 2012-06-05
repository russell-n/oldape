"""
A module to query the device for interface information (using netcfg)
"""
#python libraries
import re
from itertools import tee

from tottest.baseclass import BaseClass
from tottest.commons import enumerations
from tottest.commons import expressions


class NetcfgCommand(BaseClass):
    """
    The NetcfgCommand interprets netcfg
    """
    def __init__(self, connection, interface=None, operating_system=None):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface name (e.g. wlan0)
         - `operating_system` : The operating system on the devices.
        """
        super(NetcfgCommand, self).__init__()
        self.connection = connection
        self._interface = interface
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
            self._operating_system = enumerations.OperatingSystem.android
        return self._operating_system

    @property
    def ip_address(self):
        """
        :return: The IP Address of the interface
        """
        if self._ip_address is None:
            if self.operating_system == enumerations.OperatingSystem.android:
                expression = self.interface + expressions.NETCFG_IP
            self._ip_address = self._match(expression,
                                           expressions.IP_ADDRESS_NAME)
        return self._ip_address

    @property
    def interface(self):
        """
        :return: The name of the (presumably wireless) interface
        """
        if self._interface is None:
            expression = re.compile(expressions.NETCFG_INTERFACE)
            for line in self.output:
                match = expression.search(line)
                if match:
                    if (match.group(expressions.INTERFACE_STATE_NAME) == "UP" and
                        not match.group(expressions.IP_ADDRESS_NAME).startswith("127")):
                        self._interface = match.group(expressions.INTERFACE_NAME)
                        break
        return self._interface
    
    @property
    def mac_address(self):
        """
        :return: MAC Address of the interface
        """
        if self._mac_address is None:
            if self.operating_system == enumerations.OperatingSystem.android:
                expression = self.interface + expressions.NETCFG_IP

            self._mac_address = self._match(expression,
                                           expressions.MAC_ADDRESS_NAME)

        return self._mac_address
    
    @property
    def output(self):
        """
        This stores the value so it won't reflect updated changes.
        Does a tee so that it can be used by more than one attribute
                
        :return: The output of the netcfg command on the device
        """
        if self._output is None:
            out, self.error = self.connection.netcfg()
            self._output, output = tee(out)
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

    def __str__(self):
        return "({interface}) IP: {ip}, MAC: {mac}".format(ip=self.ip_address,
                                                           interface=self.interface,
                                                           mac=self.mac_address)
# end class IfconfigCommand
    
if __name__ == "__main__":
    from tottest.connections import adbconnection
    connection = adbconnection.ADBShellConnection()
    netcfg = NetcfgCommand(connection)
    print str(netcfg)
