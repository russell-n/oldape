"""
A command to query the dumpsys about wifi information
"""
# python
import re

from tottest.connections import adbconnection
from tottest.parsers import oatbran
from tottest.baseclass import BaseClass

class DumpsysWifiEnumerations(object):
    """
    An enumerations object
    """
    __slots__ = ()
    state = "wifistate"
    interface = "interface"
    ssid = "ssid"
    bssid = "bssid"
    mac_address = "mac_address"
    supplicant_state = "supplicant_state"
    rssi = "rssi"
    link_speed = "link_speed"
# end class DumpsysWifiEnumerations

class DumpsysWifiExpressions(object):
    """
    A class to hold regular expressions to parse the `dumpsys wifi` output
    """
    def __init__(self):
        self._state = None
        self._interface = None
        self._ssid = None
        self._bssid = None
        self._mac_address = None
        self._supplicant_state = None
        self._rssi = None
        self._link_speed = None
        return

    @property
    def state(self):
        """
        :return: compiled regular expression to match the wifi enabled/disabled states
        """
        if self._state is None:
            prefix = oatbran.SPACES.join("Wi-Fi is".split())
            suffix = oatbran.NAMED(n=DumpsysWifiEnumerations.state,
                                    e= oatbran.OR.join("enabling enabled disabled disabling".split()))
            self._state = re.compile(prefix + oatbran.SPACES + suffix)
        return self._state

    @property
    def interface(self):
        """
        :return: An expression to find the interface name
        """
        if self._interface is None:
            prefix = "[Ii]nterface" + "(Name:)" + oatbran.ZERO_OR_MORE
            expression = oatbran.NAMED(n=DumpsysWifiEnumerations.interface,
                                       e=oatbran.ALPHA_NUMS + oatbran.ONE_OR_MORE + oatbran.NATURAL)
            self._interface = re.compile(prefix + oatbran.SPACES + expression)
        return self._interface

    @property
    def ssid(self):
        """
        :return: compiled expression to extract the ssid
        """
        if self._ssid is None:
            prefix = "SSID:"
            ssid = oatbran.NAMED(n=DumpsysWifiEnumerations.ssid,
                                 e="\S[^,]" + oatbran.ZERO_OR_MORE)
            suffix = ","
            self._ssid = re.compile(prefix + oatbran.SPACES +  ssid + suffix)
        return self._ssid

    @property
    def bssid(self):
        """
        :return: compiled expression to extract the BSSID
        """
        if self._bssid is None:
            prefix = "BSSID:"
            bssid = oatbran.NAMED(n=DumpsysWifiEnumerations.bssid,
                                  e=oatbran.MAC_ADDRESS)
            suffix =  ","
            self._bssid = re.compile(prefix + oatbran.SPACES + bssid + suffix)
        return self._bssid

    @property
    def mac_address(self):
        """
        :return: compiled expression to match the MAC Address of the device
        """
        if self._mac_address is None:
            prefix = "MAC:"
            mac = oatbran.NAMED(n=DumpsysWifiEnumerations.mac_address,
                                e=oatbran.MAC_ADDRESS)
            suffix = ","
            self._mac_address = re.compile(prefix + oatbran.SPACES + mac + suffix)
        return self._mac_address

    @property
    def supplicant_state(self):
        """
        :return: compiled expression to match the WPA Supplicant State
        """
        if self._supplicant_state is None:
            prefix = "Supplicant state:"
            state = oatbran.NAMED(n=DumpsysWifiEnumerations.supplicant_state,
                                  e=oatbran.LETTERS)
            suffix = ","
            self._supplicant_state = re.compile(prefix + oatbran.SPACES + state + suffix)
        return self._supplicant_state

    @property
    def rssi(self):
        """
        :return: compiled regular expression to extract the rssi
        """
        if self._rssi is None:
            prefix = "RSSI:"
            rssi = oatbran.NAMED(n=DumpsysWifiEnumerations.rssi,
                                 e=oatbran.INTEGER)
            suffix=","
            self._rssi = re.compile(prefix + oatbran.SPACES + rssi + suffix)
        return self._rssi

    @property
    def link_speed(self):
        """
        :return: compiled regular expression to extract the link speed
        """
        if self._link_speed is None:
            prefix = "Link" + oatbran.SPACES + "speed:"
            link = oatbran.NAMED(n=DumpsysWifiEnumerations.link_speed,
                                 e=oatbran.INTEGER)
            suffix = ','
            self._link_speed = re.compile(prefix + oatbran.SPACES + link + suffix)
        return self._link_speed
# end class DumpsysWifiExpression

class DumpsysWifi(BaseClass):
    """
    A class to query and interpret the dumpsys wifi command
    """
    def __init__(self, connection=None, service="wifi", na="N/A"):
        """
        :param:

         - `connection` : connection to the DUT
         - `service`: the service to query
         - `na`: token to use if not found
        """
        super(DumpsysWifi, self).__init__()
        self._connection = connection
        self.service = service
        self.na = na
        self._state = None
        self._interface = None
        self._ssid = None
        self._bssid = None
        self._mac_address = None
        self._supplicant_state = None
        self._rssi = None
        self._link_speed = None
        
        self._expressions = None
        self.enums = DumpsysWifiEnumerations
        return

    @property
    def expressions(self):
        """
        :return: DumpsysWifiExpressions
        """
        if self._expressions is None:
            self._expressions = DumpsysWifiExpressions()
        return self._expressions

    @property
    def connection(self):
        """
        :return: a connection to the android
        """
        if self._connection is None:
            self._connection = adbconnection.ADBShellConnection()
        return self._connection

    @property
    def state(self):
        """
        :rtype: Boolean
        :return: The state of the WiFi Radio
        """
        return self.get_match(self.expressions.state, self.enums.state)

    @property
    def interface(self):
        """
        :return: name of the wifi interface
        """
        return self.get_match(self.expressions.interface, self.enums.interface)

    @property
    def ssid(self):
        """
        :return: ssid of connection
        """
        return self.get_match(self.expressions.ssid, self.enums.ssid)

    @property
    def bssid(self):
        """
        :return: bssid of the connection
        """
        return self.get_match(self.expressions.bssid, self.enums.bssid)

    @property
    def mac_address(self):
        """
        :return: MAC Address of the Wifi Interface
        """
        return self.get_match(self.expressions.mac_address, self.enums.mac_address)

    @property
    def supplicant_state(self):
        """
        :return: WPA Supplicant's state>
        """
        return self.get_match(self.expressions.supplicant_state, self.enums.supplicant_state)

    @property
    def rssi(self):
        """
        :return: the Received Signal Strength Indicator
        """
        return self.get_match(self.expressions.rssi, self.enums.rssi)

    @property
    def link_speed(self):
        """
        :return: the link speed of the WiFi connection
        """
        return self.get_match(self.expressions.link_speed, self.enums.link_speed)
    
    def get_match(self, expression, key):
        """
        :param:

         - `key`: the groupdict key to retrieve
         - `expression`: compiled expression to match field
        :return: the matching field in the output
        """
        for line in self.connection.dumpsys(self.service).output:
            self.logger.debug(line)
            match = expression.search(line)
            if match:
                return match.groupdict()[key]
        return self.na
    
    def __str__(self):
        return """State: {st}
Interface: {inter}
SSID: {ss}
BSSID: {bs}
MAC Address: {mac}
Supplicant State: {sup}
RSSI: {rs}
Link Speed: {ls}
""".format(st=self.state, inter=self.interface, ss=self.ssid, bs=self.bssid,
           mac=self.mac_address, sup=self.supplicant_state, rs=self.rssi,
           ls=self.link_speed)
# end class DumpsysWifi
    

if __name__ == "__main__":
    d = DumpsysWifi()
    print str(d)
