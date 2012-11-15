"""
An ADB device
"""

from basedevice import BaseDevice
from tottest.connections.adbconnection import ADBShellConnection
from tottest.commands.svc import Svc
from tottest.commands.netcfg import NetcfgCommand
from tottest.commands.iwcommand import IwCommand
from tottest.commands.wlcommand import WlCommand
from tottest.commands.wificommand import WifiCommand
from tottest.commands.wpacli import WpaCliCommand

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

    @property
    def wifi_info(self):
        """
        :return: wifi info summary
        """
        return
# end class AdbDevice

wifi_commands = ("wifi wl iw wpa_cli".split())

class AdbWifiCommandFinder(object):
    """
    A finder of the main wifi command.
    """
    def __call__(self, connection):
        """
        :param:

         - `connection`: An ADB Connection to the device

        :return: string identifier of primary wifi query command
        """
        commands = []
        for command in wifi_commands:
            not_found = False
            output, error = getattr(connection, command)("-h")
            for line in line:
                if "not found" in line:
                    not_found = True
                    break
            if not not_found:
                commands.append(command)
        return commands
# end class WifiCommandInventory
