"""
A Windows Device controller and queryer.
"""

from basedevice import BaseDevice
from tottest.commands.wmic import WmicWin32NetworkAdapter
from tottest.commands.netsh import NetshWlan
from tottest.commands.winrssi import WinRssi

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
        return

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
        raise NotImplementedError()    
        return

    def log(self, message):
        raise NotImplementedError()
        return

    def wake_screen(self):
        raise NotImplementedError()
        return

# end class WindowsDevice
