"""
A base module to query the device for interface information.
"""
#python libraries
from abc import ABCMeta, abstractproperty

from tottest.baseclass import BaseClass
from tottest.commons import enumerations
from tottest.commons import expressions
from tottest.commons import errors

MAC_UNAVAILABLE = "MAC Unavailable (use `netcfg`)"
CommandError = errors.CommandError


class BaseWifiCommand(BaseClass):
    """
    The Base Wifi query command
    """
    def __init__(self, connection, interface=None, operating_system=None):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface to check
         - `operating_system` : The operating system on the devices.
        """
        __metaclass__ = ABCMeta
        super(BaseWifiCommand, self).__init__()
        self._logger = None
        self.connection = connection
        self._interface = interface
        self._operating_system = operating_system
        self._rssi = None
        self._noise = None
        self._channel = None
        self._bssid = None
        self._mac_address = None
        self._ip_address = None
        return

    @property
    def operating_system(self):
        """
        :return: the operating system for the device to query
        """
        if self._operating_system is None:
            self._operating_system = self.connection.operating_system
        return self._operating_system
    
    @abstractproperty
    def interface(self):
        """
        :return: the name of the wireless interface
        """
        return self._interface

    @abstractproperty
    def rssi(self):
        """
        This is dynamically generated
        
        :return: The rssi for the interface
        """        
        return 
    
    @abstractproperty
    def mac_address(self):
        """
        :return: MAC Address of the interface
        """
        return self._mac_address
    

    def __str__(self):
        return "({iface}) RSSI: {rssi}".format(iface=self.interface,
                                               rssi=self.rssi)
# end class IfconfigCommand
    
if __name__ == "__main__":
    from tottest.connections import adbconnection
    connection = adbconnection.ADBShellConnection()
    iw = IwCommand(connection)
    print str(iw)
