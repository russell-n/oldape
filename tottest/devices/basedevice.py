"""
The Abstract Base for devices
"""
# python
from abc import ABCMeta, abstractproperty, abstractmethod

#local
from tottest.baseclass import BaseClass

class BaseDeviceEnum(object):
    __slots__ = ()
    tpc = "tpc"
    node = "node"
# end class BaseDeviceEnum
    


class BaseDevice(BaseClass):
    __metaclass__ = ABCMeta
    def __init__(self, connection=None, interface=None,
                 address=None, role=None,
                 identifier=None,
                 *args, **kwargs):
        """
        :param:

         - `connection`: An device connection
         - `interface`: The test-interface name to try and get the address
         - `address` The Test-interface IP to use if the interface name isn't given
         - `role`: an identifier to help with building file-names
         - `identifier`: A string to help identify the device
        """
        self._connection = connection
        self.interface = interface
        self.role = role
        self._address = address
        self._rssi = None
        self._wifi_info = None
        self._logger = None
        self._address = address
        return

    @property
    def connection(self):
        """
        :return: A connection to the device. 
        """
        if self._connection is None:
            self._connection = None
        return self._connection

    @abstractmethod
    def disable_wifi(self):
        """
        Disable the WiFi Radio
        """
        return

    @abstractmethod
    def enable_wifi(self):
        """
        Enable the WiFi radio.
        """
        return
    
    @abstractproperty
    def wifi_info(self):
        """
        :rtype: StringType
        :return: The Wifi Info
        """
        return

    @abstractproperty
    def address(self):
        """
        :rtype: String
        :return: the address (presumably) IP for the test-interface for the device
        """
        return

    @abstractmethod
    def log(self, message):
        """
        Send a message to the device's log.

        :param:

         - `message`: A string to send to the device log.
        """
        return

    def __str__(self):
        return "Role: {3}\nConnection: {0}\nAddress: {1}\nWiFi Info: {2}\n".format(self.connection,
                                                                                   self.address,
                                                                                   self.wifi_info,
                                                                                   self.role)
        
# end class BaseDevice
