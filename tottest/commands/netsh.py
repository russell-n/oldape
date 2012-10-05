"""
A class to make inquiries of the wlan via netsh
"""
# python
import re

from tottest.baseclass import BaseClass
from tottest.parsers import oatbran as bran
from tottest.commons.errors import CommandError

COLON = ":"

class NetshWlanExpressions(object):
    """
    A container of expressions  for the output of `netsh wlan show interfaces`
    """
    def __init__(self):
        self._authentication = None
        self._bssid = None
        self._channel = None
        self._cipher = None
        self._connection_state = None
        self._description = None
        self._mac_address = None
        self._name = None
        self._radio_type = None
        self._receive_rate = None
        self._signal = None
        self._ssid = None
        self._transmit_rate = None
        return

    @property
    def authentication(self):
        """
        :return: compiled regular expression that gets the authentication type
        """
        if self._authentication is None:
            key = "Authentication : "
            self._authentication = self.get_expression(key, NetshWlanKeys.authentication)
        return self._authentication

    @property
    def bssid(self):
        """
        :return: compiled regular expression to get the BSSID
        """
        if self._bssid is None:
            key = "BSSID : "
            self._bssid = self.get_expression(key, NetshWlanKeys.bssid)
        return self._bssid

    @property
    def channel(self):
        """
        :return: compiled regular expression to get the channel
        """
        if self._channel is None:
            key= "Channel : "
            self._channel = self.get_expression(key, NetshWlanKeys.channel)
        return self._channel

    @property
    def cipher(self):
        """
        :return: compiled regular expression to get the authentication cipher
        """
        if self._cipher is None:
            key = "Cipher                 : "
            self._cipher = self.get_expression(key, NetshWlanKeys.cipher)
        return self._cipher

    @property
    def connection_state(self):
        """
        :return: compiled regular expression to get the connection state
        """
        if self._connection_state is None:
            key = "State                  : "
            self._connection_state = self.get_expression(key, NetshWlanKeys.connection_state)
        return self._connection_state

    @property
    def description(self):
        """
        :return: compiled regular expression to get the interface model 
        """
        if self._description is None:
            key = "Description            : "
            self._description = self.get_expression(key, NetshWlanKeys.description)
        return self._description

    @property
    def mac_address(self):
        """
        :return: compiled regular expression to get the MAC Address of the interface
        """
        if self._mac_address is None:
            key = "Physical address       : "
            self._mac_address = self.get_expression(key, NetshWlanKeys.mac_address)
        return self._mac_address

    @property
    def name(self):
        """
        :return: compiled regular expression to match names
        """
        if self._name is None:
            key = "Name : "
            self._name = self.get_expression(key, NetshWlanKeys.name)
        return self._name

    @property
    def radio_type(self):
        """
        :return: compiled regular expression to match the radio type
        """
        if self._radio_type is None:
            key = "Radio type             : "
            self._radio_type = self.get_expression(key, NetshWlanKeys.radio_type)
        return self._radio_type

    @property
    def receive_rate(self):
        """
        :return: compiled regular expression to match receive rate        
        """
        if self._receive_rate is None:
            key = "Receive rate \(Mbps\)    : "
            value = bran.NAMED(n=NetshWlanKeys.receive_rate,
                               e=bran.NATURAL)
            self._receive_rate = re.compile(bran.SPACES.join((key +value).split()))
        return self._receive_rate
    
    @property
    def signal(self):
        """
        :return: compiled regular expression to get the signal
        """
        if self._signal is None:
            key = "Signal : "
            value = bran.NAMED(n=NetshWlanKeys.signal,
                               e=bran.NATURAL + "%")
            self._signal = re.compile(bran.SPACES.join((key + value).split()))
        return self._signal

    @property
    def ssid(self):
        """
        :return: compiled regular expression to get the ssid
        """
        if self._ssid is None:
            key = "SSID : "
            self._ssid = self.get_expression(key, NetshWlanKeys.ssid)
        return self._ssid

    @property
    def transmit_rate(self):
        """
        :return: compiled regular expression to get the transmit rate
        """
        if self._transmit_rate is None:
            
            key = "Transmit rate \(Mbps\) : "
            self._transmit_rate = self.get_expression(key, NetshWlanKeys.transmit_rate)
            
        return self._transmit_rate

    def get_expression(self, key, name):
        """
        :return: expression that matches anything in the value column
        """
        value = bran.NAMED(n=name,e=bran.ANYTHING_BOUNDED_BY_SPACES)
        return re.compile(bran.SPACES.join((key + value).split()))
    
class NetshWlanKeys(object):
    __slots__ = ()
    authentication = "Authentication"
    bssid = "BSSID"
    channel = "Channel"
    cipher = "Cipher"
    connection_state = "State"
    description = "Description"
    mac_address = "Physical"
    name = "Name"
    radio_type = "Radio"
    receive_rate = "Receive"
    signal = "Signal"
    ssid = "SSID"
    transmit_rate = "Transmit"
# end class NetshWlanExpressions

class NetshWlan(BaseClass):
    """
    A querier for basic netsh information
    """
    def __init__(self, connection, separator=":", not_available="NA"):
        """
        :param:

         - `connection`: A connection to the device with netsh
         - `separator`: The column delimiter
         - `not_available`: token to return if the field wasn't populated
        """
        super(NetshWlan, self).__init__()
        self.connection = connection
        self.separator = separator
        self.not_available = not_available
        self._output = None
        self._expressions = None
        self._signal = None
        return

    @property
    def signal(self):
        """
        :return: signal %
        """
        output, error = self.connection.netsh("wlan show interface")
        for line in output:
            match =  self.expressions.signal.search(line)
            if match:
                return match.groupdict()[NetshWlanKeys.signal]
        return self.not_available

    @property
    def output(self):
        """
        :return: stdout as a list
        """
        if self._output is None:
            output = self.connection.netsh("wlan show interface")
            self._output = output.output
            self.check_errors(output.error)
        return self._output
        
    @property
    def expressions(self):
        """
        :return: Netsh wlan regular expressions
        """
        if self._expressions is None:
            self._expressions = NetshWlanExpressions()
        return self._expressions

    def get_value(self, expression, key):
        """
        :return: the value from netsh's output that matches the key
        """
        self.logger.debug("expression: {0}, key: {1}".format(expression, key))
        output = self.connection.netsh("wlan show interface", max_time=30)

        for line in output.output:
            match =  expression.search(line)
            if match:
                return match.groupdict()[key]
        self.check_errors(output.error)
        return self.not_available

    def check_errors(self, stderr):
        """
        :param:

         - `stderr`: file output of stderr
        """
        # make a jazz noise here
        self.logger.debug("Checking for errors")
        for line in stderr:
            self.logger.error(line)
            if "no wireless interface" in line:
                raise CommandError(line)
        return

    def reset(self):
        """
        :postcondition: self._output is None
        """
        self._output = None
        return

                              
    def __getattr__(self, prop):
        """
        :param:

         - `property`: A valid property (use NetshWlanKeys properties)
        """
        try:
            return self.get_value(getattr(self.expressions, prop), getattr(NetshWlanKeys, prop))
        except AttributeError as error:
            self.logger.error(error)
            raise CommandError("Unknown (or unimplemented) Field: {0}".format(prop))
# end class NetshWlan
