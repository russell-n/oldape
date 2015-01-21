"""
A module to query a mac for interface information.
"""
#python libraries
import re
from collections import defaultdict

#apetools
from apetools.commons import errors
import apetools.commons.expressions as expressions
from basewificommand import BaseWifiCommand
CommandError = errors.CommandError

NA = 'NA'

WORD_BOUNDARY = r'\b'
SPACE = r'\s'
ONE_OR_MORE = '+'
SPACES = SPACE + ONE_OR_MORE
BASE_EXPRESSION = WORD_BOUNDARY + '{0}:'   + SPACES + '(.*)'

class AirportCommandError(CommandError):
    """
    An error to raise if the Wifi Command fails
    """
# end class WifiCommandError


class AirportCommand(BaseWifiCommand):
    """
    The Wifi Command interprets `airport` information

    """
    def __init__(self, airport_command='airport --getinfo', 
                 *args, **kwargs):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface to check
         - `airport_command`: Command to get the info from airport
        """
        super(AirportCommand, self).__init__(*args, **kwargs)
        self.airport_command = airport_command
        self._expressions = None
        self._mac_expression = None
        self._ip_address = None
        self._ip_expression = None
        return

    @property
    def ip_expression(self):
        if self._ip_expression is None:
            expression = (expressions.SPACES + 'inet'
                          + expressions.SPACES + 
                          expressions.IP_ADDRESS)
            self._ip_expression = re.compile(expression)
        return self._ip_expression

    @property
    def ip_address(self):
        with self.connection.lock:
            output, error = self.connection.ifconfig(self.interface)
        interface = False
        for line in output:
            if not interface:
                interface = line.startswith(self.interface)
                continue
            match = self.ip_expression.search(line)
            if match:
                return match.groupdict()[expressions.IP_ADDRESS_NAME]
        err = error.readline()
        if err:
            self.logger.error("Unable to get ip for {0}".format(self.connection))
            raise Exception(err)    
        return 

    @property
    def mac_expression(self):
        if self._mac_expression is None:
            expression = 'ether' + expressions.SPACES + expressions.MAC_ADDRESS
            self._mac_expression = re.compile(expression)
        return self._mac_expression

    @property
    def expressions(self):
        if self._expressions is None:
            self._expressions = defaultdict(lambda : None)
        return self._expressions
   
    @property
    def bitrate(self):
        """
        :return: the max bitrate if found
        """
        return self.get("lastTxRate")
    
    @property
    def interface(self):
        """
        :return: the name of the wireless interface
        """
        if self._interface is None:
            self.logger.warning("interface name not set")
        return self._interface

    @property
    def rssi(self):
        """
        This is dynamically generated
        
        :return: The rssi for the interface
        """
        return self.get("agrCtlRSSI")
    
    @property
    def mac_address(self):
        """
        :return: MAC Address of the interface
        """
        if self._mac_address is None:
            interface = False
            MAC_ADDRESS_NAME = expressions.MAC_ADDRESS_NAME
            with self.connection.lock:
                output, error = self.connection.ifconfig(self.interface)
            for line in output:
                if not interface:
                    interface = line.startswith(self.interface)
                    continue
                match = self.mac_expression.search(line)
                if match:
                    self._mac_address = match.groupdict()[MAC_ADDRESS_NAME]
                    break        
            err = error.readline()
            if err:
                raise AirportCommand(err)
        return self._mac_address

    @property
    def ssid(self):
        """
        :return: the SSID of the currently attched ap
        """
        return self.get('SSID')

    @property
    def noise(self):
        """
        :return: the current noise
        """
        return self.get('agrCtlNoise')

    @property
    def channel(self):
        """
        :return: the current channel setting
        """
        return self.get('channel')


    @property
    def bssid(self):
        """
        :return: the bssid of the attached ap
        """
        return self.get('BSSID')
    
        
    def get(self, token):
        """
        :param:

         - `token`: token to look for in the airport output

        
        :return: value that matches the token
        """
        with self.connection.lock:
            output, error = self.connection.airport(self.airport_command)

        if self.expressions[token] is None:
            self.expressions[token] = re.compile(BASE_EXPRESSION.format(token))
        expression = self.expressions[token]
        for line in output:
            match = expression.search(line)
            if match:
                return match.groups()[-1]
        err = error.readline()
        if len(err):
            self.logger.error(err)
            if "No such device" in err:
                raise CommandError("Unknown Interface: {0}".format(self.interface))
            else:
                raise CommandError(err)
        return

    def status(self):
        return "MAC: {0}\nIP: {2}\n{1}\n".format(self.mac_address,
                                                 str(self),
                                                 self.ip_address)
    
    def __str__(self):
        return "".join([line for line in self.connection.airport(self.airport_command)])
# end class WifiCommand
    
if __name__ == "__main__":
    from mock import MagicMock
    from StringIO import StringIO
    OUTPUT = """
     agrCtlRSSI: -79
     agrExtRSSI: 0
    agrCtlNoise: -89
    agrExtNoise: 0
          state: running
        op mode: station 
     lastTxRate: 216
        maxRate: 450
lastAssocStatus: 0
    802.11 auth: open
      link auth: wpa2-psk
          BSSID: 84:1b:5e:da:34:8
           SSID: r6300_5
            MCS: 13
        channel: 36,1
        """
    
    connection = MagicMock()
    command = AirportCommand(connection=connection,
                                      interface='wlan0')

    connection.airport.return_value = StringIO(OUTPUT), StringIO("")
    import pudb;pudb.set_trace()
    print command.ssid

