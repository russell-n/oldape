"""
An ADB device
"""

from tottest.baseclass import BaseClass 
from basedevice import BaseDevice
from tottest.connections.adbconnection import ADBShellConnection
from tottest.commands.svc import Svc
from tottest.commands.netcfg import NetcfgCommand
from tottest.commands.iwcommand import IwCommand
from tottest.commands.wlcommand import WlCommand
from tottest.commands.wificommand import WifiCommand
from tottest.commands.wpacli import WpaCliCommand

from tottest.commons.errors import CommandError

commands = {"iw":IwCommand,
            'wl':WlCommand,
            'wifi':WifiCommand,
            'wpa_cli':WpaCliCommand}

class AdbDevice(BaseDevice):
    """
    A class to bundle commands to control an adb device
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: An device connection
        """
        super(AdbDevice, self).__init__(*args, **kwargs)
        self._wifi_control = None
        self._wifi_querier = None
        self._netcfg = None
        self._wifi_commands = None
        return

    @property
    def channel(self):
        """
        :return: the channel for the current wifi connection
        """
        return self.wifi_querier.channel
    
    @property
    def rssi(self):
        """
        :return: the current RSSI
        """
        return self.wifi_querier.rssi

    @property
    def noise(self):
        """
        :return: the current noise
        """
        return self.wifi_querier.noise

    @property
    def ssid(self):
        """
        :return: the ssid of the attached AP
        """
        return self._wifi_querier.ssid

    @property
    def bssid(self):
        """
        :return: the MAC address of the attached AP
        """
        return self._wifi_querier.bssid
    
    @property
    def mac_address(self):
        """
        :return: devices mac address
        """
        if self._mac_address is None:
            if "wpa_cli" in self.wifi_commands:
                self._mac_address = commands['wpa_cli'](connection=self.connection,
                                                        interface=self.interface).mac_address
            else:
                self._mac_address = self.wifi_querier.mac_address
        return self._mac_address
    
    @property
    def wifi_commands(self):
        """
        :return: list of available wifi commands
        """
        if self._wifi_commands is None:
            self._wifi_commands = AdbWifiCommandFinder()(self.connection)
        return self._wifi_commands
    
    @property
    def wifi_querier(self):
        """
        :return: command to query wifi information
        """
        if self._wifi_querier is None:
            self._wifi_querier = commands[self.wifi_commands[0]](connection=self.connection,
                                                   interface=self.interface)
        return self._wifi_querier

    @property
    def netcfg(self):
        """
        :return: NetcfgCommand
        """
        if self._netcfg is None:
            self._netcfg = NetcfgCommand(self.connection,
                                         self.interface)
        return self._netcfg

    @property
    def wifi_control(self):
        """
        :return: Svc command (enable disable radio)
        """
        if self._wifi_control is None:
            self._wifi_control = Svc(connection=self.connection)
        return self._wifi_control

    @property
    def connection(self):
        """
        :return: connection passed in or ADBShellConnection if not given
        """
        if self._connection is None:
            self._connection = ADBShellConnection()
        return self._connection

    def wake_screen(self):
        """
        Wake the screen
        """
        raise NotImplementedError("Wake Screen not ready yet")
        return

    def display(self, message):
        """
        Display a message on the screen
        """
        raise NotImplementedError("Display <message> not done yet")
        return

    def disable_wifi(self):
        """
        :postcondition: WiFi radio disabled
        """
        self.wifi_control.disable_wifi()
        return

    def enable_wifi(self):
        """
        :postcondition: WiFi radio enabled
        """
        self.wifi_control.enable_wifi()
        return

    def get_wifi_info(self):
        """
        :rtype: StringType
        :return: The Wifi Info
        """
        
        raise NotImplementedError("Get WiFi Info not done yet")
        return

    def log(self, message):
        """
        :postcondition: message sent to the connection
        """
        self.connection.log(message)
        return

    def root(self):
        """
        :postcondition: `su` sent to the device
        """
        self.connection.su(timeout=1)
        return

    @property
    def address(self):
        """
        :return: ip address of interface
        """
        return self.netcfg.ip_address                         
        
# end class AdbDevice

wifi_commands = ("wifi wl iw wpa_cli".split())

class AdbWifiCommandFinder(BaseClass):
    """
    A finder of the main wifi command.
    """
    def __call__(self, connection):
        """
        :param:

         - `connection`: An ADB Connection to the device

        :return: string identifier of primary wifi query command
        """
        super(AdbWifiCommandFinder, self).__init__()
        commands = []
        for command in wifi_commands:
            try:
                output, error = getattr(connection, command)("-v")
                for line in output:
                    self.logger.debug(line)
                commands.append(command)
            except CommandError as error:
                self.logger.debug(error)
        return commands
# end class WifiCommandInventory

if __name__ == "__main__":
    from tottest.connections.adbconnection import ADBShellSSHConnection
    import sys
    c = ADBShellSSHConnection(hostname="lancet", username="allion")
    a = AdbDevice(connection = c, interface="wlan0", csv=True)
    sys.stdout.write(a.wifi_info)
    sys.stdout.write(a.wifi_info)
    
