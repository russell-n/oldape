"""
A configurer and queryier for linux devices.
"""

from apetools.commands.ifconfig import IfconfigCommand
from apetools.commands.iwconfig import Iwconfig
from apetools.commons.enumerations import OperatingSystem
from apetools.devices.basedevice import BaseDevice

class LinuxDevice(BaseDevice):
    """
    A class to configure and query linux devices
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: a connection to the device
         - `interface`: the name of the test interface (to get the ip address)
        """
        super(LinuxDevice, self).__init__(*args, **kwargs)
        self._ifconfig = None
        self._wifi_query = None
        return

    @property
    def ifconfig(self):
        """
        :return: ifconfig command
        """
        if self._ifconfig is None:
            self._ifconfig = IfconfigCommand(connection=self.connection,
                                             interface = self.interface,
                                             operating_system=OperatingSystem.linux)
        return self._ifconfig

    @property
    def wifi_query(self):
        """
        :return: wifi_query command
        """
        if self._wifi_query is None:
            self._wifi_query = Iwconfig(connection=self.connection,
                                      interface=self.interface)
        return self._wifi_query

    @property
    def address(self):
        """
        :return: the address of the device
        """
        if self._address is None:
            return self.ifconfig.ip_address
        return

    @property
    def mac_address(self):
        """
        :return: the MAC address of the device
        """
        return self.ifconfig.mac_address

    @property
    def bssid(self):
        return self.wifi_query.bssid
    
    @property
    def ssid(self):
        return self.wifi_query.ssid

    @property
    def noise(self):
        return "NA"

    @property
    def channel(self):
        return "NA"
    
    @property
    def rssi(self):
        """
        :return: rssi from the wifi_query
        """
        return self.wifi_query.rssi

    @property
    def bitrate(self):
        """
        :return: bitrate from the wifi_query
        """
        return self.wifi_query.bitrate

    def disable_wifi(self):
        self.connection.rfkill("block wifi")
        return

    def enable_wifi(self):
        self.connection.rfkill("unblock wifi")
        return

    def log(self, message):
        """
        :param:

         - `message`: a string to send to the syslog

        :postcondition: message sent to the syslog
        """
        self.connection.logger(message)
        return
# end class LinuxDevice
