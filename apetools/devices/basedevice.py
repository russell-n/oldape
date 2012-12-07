"""
The Abstract Base for devices
"""
# python
from abc import ABCMeta, abstractproperty, abstractmethod

#local
from apetools.baseclass import BaseClass

class BaseDeviceEnum(object):
    __slots__ = ()
    tpc = "tpc"
    node = "node"
# end class BaseDeviceEnum
    
CSV_OUTPUT = "{ssid},{bssid},{channel},{ip},{mac},{rssi},{noise}\n"
HUMAN_OUTPUT = """
SSID        = {ssid}
BSSID       = {bssid}
Channel     = {channel}
IP Address  = {ip}
MAC Address = {mac}
RSSI        = {rssi}
Noise       = {noise}
"""

class BaseDevice(BaseClass):
    __metaclass__ = ABCMeta
    def __init__(self, connection=None, interface=None,
                 address=None, role=None,
                 csv=False,
                 *args, **kwargs):
        """
        :param:

         - `connection`: An device connection
         - `interface`: The test-interface name to try and get the address
         - `address` The Test-interface IP to use if the interface name isn't given
         - `role`: an identifier to help with building file-names
         - `csv`: if True, queries are output as CSV
        """
        self._connection = connection
        self.interface = interface
        self.role = role
        self.csv = csv
        self._address = address
        self._rssi = None
        self._ssid = None
        self._bssid = None
        self._noise = None
        self._wifi_info = None
        self._logger = None
        self._mac_address = None
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

    @property
    def wifi_info(self):
        """
        :return: wifi info summary
        """
        if self.csv:
            out_string = CSV_OUTPUT
        else:
            out_string = HUMAN_OUTPUT

        return out_string.format(ip=self.address.rstrip(),
                                 rssi=self.rssi.rstrip(),
                                 ssid=self.ssid.rstrip(),
                                 bssid=self.bssid.rstrip(),
                                 channel=self.channel.rstrip(),
                                 noise=self.noise.rstrip(),
                                 mac=self.mac_address.rstrip())
    
    @abstractproperty
    def address(self):
        """
        :rtype: String
        :return: the address (presumably) IP for the test-interface for the device
        """
        return

    @abstractproperty
    def ssid(self):
        """
        :return: the SSID of the attached AP
        """
        return self._ssid

    @abstractproperty
    def bssid(self):
        """
        :return: the MAC address of the attached AP
        """
        return self._bssid

    @abstractproperty
    def channel(self):
        """
        :return: the channel for the wifi connection
        """
        return self._channel

    @abstractproperty
    def noise(self):
        """
        :return: the current reported noise for the wifi channel
        """
        return self._noise

    @abstractproperty
    def mac_address(self):
        """
        :return: the mac address of the device
        """
        return self._mac_address

    @abstractproperty
    def rssi(self):
        """
        :return: the RSSI for the wifi signal
        """
        return self._rssi
    
    @abstractmethod
    def log(self, message):
        """
        Send a message to the device's log.

        :param:

         - `message`: A string to send to the device log.
        """
        return

    def __str__(self):
        return "Role: {2}\nConnection: {0}\nWiFi Info: {1}\n".format(self.connection,
                                                                     self.wifi_info,
                                                                     self.role)
        
# end class BaseDevice
