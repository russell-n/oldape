
from apetools.baseclass import BaseClass
from apetools.commands import wpacli, iwcommand, netcfg
from apetools.connections import adbconnection


class WifiToolAdb(BaseClass):
    """
    The WifiTool aggregates wifi commands
    """
    def __init__(self, status_command=None,
                 ip_command=None,
                 interface_command=None,
                 mac_command=None,
                 rssi_command=None,
                 ssid_command=None):
        super(WifiToolAdb, self).__init__()
        self._status_command = status_command
        self._ip_command = ip_command
        self._interface_command = interface_command
        self._mac_command = mac_command
        self._rssi_command = rssi_command
        self._ssid_command = ssid_command
        self._wpacli_command = None
        self._iw_command = None
        self._netcfg = None
        self._connection = None
        return

    @property
    def netcfg(self):
        """
        :return: The netcfg command
        """
        if self._netcfg is None:
            self._netcfg = netcfg.NetcfgCommand(self.connection)
        return self._netcfg

    @property
    def iw_command(self):
        """
        :return: The `iw` command
        """
        if self._iw_command is None:
            self._iw_command = iwcommand.IwCommand(connection=self.connection)
        return self._iw_command
    
    @property
    def wpacli_command(self):
        """
        :return: A `wpa_cli` command object 
        """
        if self._wpacli_command is None:
            self._wpacli_command = wpacli.WpaCliCommand(connection=self.connection)
        return self._wpacli_command

    @property
    def connection(self):
        """
        :return: The device connection
        """
        if self._connection is None:
            self._connection = adbconnection.ADBShellConnection()
        return self._connection
    
    @property
    def status_command(self):
        """
        :return: The command to get the wifi status string
        """
        if self._status_command is None:
            self._status_command = self.wpacli_command
        return self._status_command

    @property
    def ip_command(self):
        """
        :return: A Command to get the ip address
        """
        if self._ip_command is None:
            self._ip_command = self.wpacli_command
        return self._ip_command

    @property
    def interface_command(self):
        """
        :return: A command to get the wifi interface name
        """
        if self._interface_command is None:
            self._interface_command = self.wpacli_command
        return self._interface_command

    @property
    def mac_command(self):
        """
        :return: A command to get the mac address
        """
        if self._mac_command is None:
            self._mac_command = self.wpacli_command
        return self._mac_command

    @property
    def rssi_command(self):
        """
        :return: A command to get the rssi
        """
        if self._rssi_command is None:
            self._rssi_command = self.iw_command
        return self._rssi_command

    @property
    def ssid_command(self):
        """
        :return: A command to get the ssid
        """
        if self._ssid_command is None:
            self._ssid_command = self.wpacli_command
        return self._ssid_command

    def __str__(self):
        return self.status_command.status + "\n" + self.rssi_command.rssi
    
# end class WifiToolAdb
