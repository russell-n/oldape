"""
A Windows Device controller and queryer.
"""

from basedevice import BaseDevice
from tottest.commands.wmic import WmicWin32NetworkAdapter
from tottest.commands.netsh import NetshWlan
from tottest.commands.winrssi import WinRssi
from tottest.commands.ipconfig import Ipconfig
from tottest.commands.windowsssidconnect import WindowsSSIDConnect

class WindowsDevice(BaseDevice):
    """
    A class to control and query windows devices
    """
    def __init__(self, connection):
        super(WindowsDevice, self).__init__()
        self._connection = connection
        self._wifi_control = None
        self._wifi_query = None
        self._rssi_query = None
        self._ipconfig = None
        self._ssid_connect = None
        self._address = None
        return

    @property
    def ssid_connect(self):
        """
        :return: a Windows SSID Connect command
        """
        if self._ssid_connect is None:
            self._ssid_connect = WindowsSSIDConnect(self.connection)
        return self._ssid_connect

    @property
    def ipconfig(self):
        """
        :return: the Ipconfig
        """
        if self._ipconfig is None:
            self._ipconfig = Ipconfig(self.connection)
        return self._ipconfig

    @property
    def wifi_control(self):
        """
        :return: WmicWin32NetworkAdapter
        """
        if self._wifi_control is None:
            self._wifi_control = WmicWin32NetworkAdapter(self.connection)
        return self._wifi_control

    @property
    def rssi_query(self):
        """
        :return: WinRssi querier
        """
        if self._rssi_query is None:
            self._rssi_query = WinRssi(self.connection)
        return self._rssi_query

    @property
    def rssi(self):
        """
        :return: the current rssi on the device
        """
        return self.rssi_query()
    
    @property
    def wifi_info(self):
        """
        :return: String containing the wifi info
        """
        return "\n".join([line for line in self.wifi_query.output] +
                         ["rssi: {0} dbm".format(self.rssi_query())])

    @property
    def wifi_query(self):
        """
        :return: a NetshWlan query
        """
        if self._wifi_query is None:
            self._wifi_query = NetshWlan(self.connection)
        return self._wifi_query

    
    @property
    def address(self):
        """
        :return: the IP Address of the wireless interface
        """
        return self.ipconfig.address
    
    def enable_wifi(self):
        """
        :postcondition: `wmic` called to enable the radio
        """
        self.wifi_control.enable_wifi()
        return
    
    def disable_wifi(self):
        """
        :postcondition: `wmic` called to disable radio
        """
        self.wifi_control.disable_wifi()
        return

    def display(self, message):
        self.logger.warning("Display not implemented")
        return

    def log(self, message):
        self.connection.eventcreate('/l System /id 999 /d "{0}" /t Information /so Private'.format(message))
        return

    def wake_screen(self):
        self.logger.warning("Wake-Screen Not Implemented")
        return

    def connect(self, ssid):
        """
        :param:

         - `ssid`: The SSID and Profile name to connect to
        """
        self.ssid_connect(ssid)
        return

    def disconnect(self):
        """
        :postcondition: the device is disconnected from the AP but no disabled
        """
        self.connection.netsh("wlan disconnect")
        return
# end class WindowsDevice
