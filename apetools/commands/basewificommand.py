
#python libraries
from abc import ABCMeta, abstractproperty

from apetools.baseclass import BaseClass
from apetools.commons import errors


MAC_UNAVAILABLE = "MAC Unavailable (use `netcfg`)"
CommandError = errors.CommandError


class BaseWifiCommand(BaseClass):
    """
    The Base Wifi query command
    """
    __metaclass__ = ABCMeta
    def __init__(self, connection, interface=None, operating_system=None):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface to check
         - `operating_system` : The operating system on the devices.
        """
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
        self._bitrate = None
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
    def bitrate(self):
        """
        :return: the reported physical bit-rate
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
# end class BaseWifiCommand
