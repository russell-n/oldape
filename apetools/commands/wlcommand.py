
#python libraries
import re

# this package
from apetools.commons import errors

from basewificommand import BaseWifiCommand


MAC_UNAVAILABLE = "MAC Unavailable (use `netcfg`)"
CommandError = errors.CommandError


class WlCommand(BaseWifiCommand):
    """
    The Wl Command interprets WL information
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface to check
         - `operating_system` : The operating system on the devices.
        """
        super(WlCommand, self).__init__(*args, **kwargs)
        return
    
    @property
    def interface(self):
        """
        :return: the name of the wireless interface
        """
        if self._interface is None:
            self.logger.warning("wl doesn't use the interface name")
        return self._interface

    @property
    def rssi(self):
        """
        This is dynamically generated
        
        :return: The rssi for the interface
        """
        output = self.get("rssi")
        return output.readline()
    
    @property
    def mac_address(self):
        """
        :return: MAC Address of the interface
        """
        if self._mac_address is None:
            output = self.get("mac")
            self._mac_address = output.readline()
        return self._mac_address

    @property
    def bitrate(self):
        """
        :return: the reported physical bitrate
        """
        return self.get("rate").readline().split()[0]

    @property
    def ssid(self):
        """
        :return: the SSID of the currently attched ap
        """
        output = self.get('ssid')
        return output.readline().split(":")[-1]

    @property
    def noise(self):
        """
        :return: the current noise
        """
        return self.get('noise').readline()

    @property
    def channel(self):
        """
        :return: the current channel setting
        """
        output = self.get('status')
        for line in output:
            if "Control channel:" in line:
                return line.split(":")[-1].strip()
        return

    @property
    def bssid(self):
        """
        :return: the bssid of the attached ap
        """
        return self.get('bssid').readline()
    
    def get(self, subcommand):
        """
        :param:

         - `subcommand`: `wl` subcommand

        :return: stdout for the command
        """
        with self.connection.lock:
            output, error = self.connection.wl(subcommand)
        err = error.readline()
        if len(err) > 1:
            self.logger.error(err)
        return output
        
    def _match(self, expression, name, command):
        """
        :param:

         - `expression`: The regular expression to match
         - `name`: The group name to pull the match out of the line
         - `command`: The command to send to iw
         
        :return: The named-group that matched or None
        """
        expression = re.compile(expression)
        with self.connection.lock:
            output, error = self.connection.iw(command)
        for line in output:
            match = expression.search(line)
            if match:
                return match.group(name)
        err = error.read()
        if len(err):
            self.logger.error(err)
            if "No such device" in err:
                raise CommandError("Unknown Interface: {0}".format(self.interface))
            else:
                raise CommandError(err)
        return

    def __str__(self):
        return "({iface}) RSSI: {rssi}".format(iface=self.interface,
                                               rssi=self.rssi)
# end class WlCommand


if __name__ == "__main__":
    from apetools.connections import adbconnection
    connection = adbconnection.ADBShellConnection()
    iw = IwCommand(connection)
    print str(iw)
