from unittest import TestCase
from StringIO import StringIO

from mock import MagicMock

from apetools.commands import netsh
from apetools.connections.sshconnection import OutputError
from apetools.commons import errors
CommandError = errors.CommandError

OUTPUT = """
There is 1 interface on the system:

    Name                   : Wireless Network Connection
    Description            : Intel(R) Centrino(R) Wireless-N 100
    GUID                   : 580dc1eb-f5cd-4eb9-8483-cff1a9e2f0f8
    Physical address       : 78:92:9c:8d:e1:5e
    State                  : connected
    SSID                   : allionstaff
    BSSID                  : 18:33:9d:f9:ad:10
    Network type           : Infrastructure
    Radio type             : 802.11g
    Authentication         : WPA2-Personal
    Cipher                 : CCMP
    Connection mode        : Auto Connect
    Channel                : 6
    Receive rate (Mbps)    : 72
    Transmit rate (Mbps)   : 72
    Signal                 : 99%
    Profile                : allionstaff

    Hosted network status  : Not started"""

class TestNetsh(TestCase):
    def setUp(self):
        output = StringIO(OUTPUT)
        self.output = OutputError(output, "")
        self.connection = MagicMock()
        self.connection.netsh.return_value = self.output
        self.netsh = netsh.NetshWlan(connection=self.connection)
        return

    def test_output(self):
        for line in self.netsh.output:
            self.assertIn(line, OUTPUT)            
        return
    
    def test_authentication(self):
        expected = "WPA2-Personal"
        actual = self.netsh.authentication
        self.assertEqual(expected, actual)
        return

    def test_bssid(self):
        expected = "18:33:9d:f9:ad:10"
        actual = self.netsh.bssid
        self.assertEqual(expected, actual)
        return

    def test_channel(self):
        expected = "6"
        actual = self.netsh.channel
        self.assertEqual(expected, actual)
        return

    def test_cipher(self):
        expected = "CCMP"
        actual = self.netsh.cipher
        self.assertEqual(expected,actual)
        return
    
    def test_connection_state(self):
        expected = "connected"
        actual = self.netsh.connection_state
        self.assertEqual(expected, actual)
        return

    def test_description(self):
        expected = "Intel(R) Centrino(R) Wireless-N 100"
        actual = self.netsh.description
        self.assertEqual(expected, actual)
        return

    def test_mac(self):
        expected = "78:92:9c:8d:e1:5e"
        actual = self.netsh.mac_address
        self.assertEqual(expected,actual)
        return
    
    def test_name(self):
        expected = "Wireless Network Connection"
        actual = self.netsh.name
        self.assertEqual(expected, actual)
        return

    def test_receive_rate(self):
        expected = "72"
        actual = self.netsh.receive_rate
        self.assertEqual(expected, actual)
        return
    
    def test_radio_type(self):
        expected = "802.11g"
        actual = self.netsh.radio_type
        self.assertEqual(expected, actual)
        return
    
    def test_signal(self):
        expected = "99%"
        actual = self.netsh.signal
        self.assertEqual(expected, actual)
        return
        
    def test_ssid(self):
        expected = "allionstaff"
        actual = self.netsh.ssid
        self.assertEqual(expected, actual)
        return
    
    def test_transmit_rate(self):
        expected = "72"
        actual = self.netsh.transmit_rate
        self.assertEqual(expected,actual)
        return

    def test_failure(self):
        output = OutputError("", StringIO("There is no wireless interface on the system.\nHosted network status  : Not available\n"))
        connection = MagicMock()
        connection.netsh.return_value = output
        _netsh = netsh.NetshWlan(connection=connection)
        with self.assertRaises(errors.CommandError):
            _netsh.ssid
        return

    def test_unknown_field(self):
        with self.assertRaises(CommandError):
            self.netsh.gumballs
        return

    def test_not_avalable(self):
        output = OutputError("", "")
        connection = MagicMock()
        connection.netsh.ssid.return_value = output
        _netsh = netsh.NetshWlan(connection=connection)
        expected = _netsh.not_available
        actual = _netsh.ssid
        self.assertEqual(expected, actual)
        return

# end TestNetshWlan

        
class TestNetshWlanExpressions(TestCase):
    def setUp(self):
        self.expressions = netsh.NetshWlanExpressions()
        self.keys = netsh.NetshWlanKeys
        return

    def check_expression(self, output, expression, key, expected):
        print key
        print output
        match = expression.search(output)
        self.assertEqual(expected, match.groupdict()[key])
        return
    
    def test_name(self):
        self.check_expression("    Name                   : Wireless Network Connection",
                              self.expressions.name,
                              self.keys.name,
                              "Wireless Network Connection")
        return

    def test_description(self):
        self.check_expression("    Description            : Intel(R) Centrino(R) Wireless-N 100",
                              self.expressions.description,
                              self.keys.description,
                              "Intel(R) Centrino(R) Wireless-N 100")
        return

    def test_mac_address(self):
        self.check_expression("    Physical address       : 78:92:9c:8d:e1:5e",
                              self.expressions.mac_address,
                              self.keys.mac_address,
                              "78:92:9c:8d:e1:5e")
        return

    def test_connection_state(self):
        self.check_expression("    State                  : connected",
                       self.expressions.connection_state,                       
                       self.keys.connection_state,
                       "connected")
        self.check_expression("    State                  : disconnected",
                       self.expressions.connection_state,                       
                       self.keys.connection_state,
                       "disconnected")

        return

    def test_ssid(self):
        self.check_expression("    SSID                   : allionstaff",
                              self.expressions.ssid,
                              self.keys.ssid,
                              "allionstaff")
        return

    def test_bssid(self):
        self.check_expression("    BSSID                  : 18:33:9d:f9:ad:10",
                              self.expressions.bssid,
                              self.keys.bssid,
                              "18:33:9d:f9:ad:10")
        return

    def test_radio_type(self):
        self.check_expression("    Radio type             : 802.11g",
                              self.expressions.radio_type,
                              self.keys.radio_type,
                              "802.11g")
        return

    def test_authentication(self):
        self.check_expression("    Authentication         : WPA2-Personal",
                              self.expressions.authentication,
                              self.keys.authentication,
                              "WPA2-Personal")
        return

    def test_cipher(self):
        self.check_expression("    Cipher                 : CCMP",
                              self.expressions.cipher,
                              self.keys.cipher,
                              "CCMP")
        return

    def test_channel(self):
        self.check_expression("    Channel                : 6",
                              self.expressions.channel,
                              self.keys.channel,
                              "6")
        return

    def test_receive_rate(self):
        self.check_expression("    Receive rate (Mbps)    : 72",
                              self.expressions.receive_rate,
                              self.keys.receive_rate,
                              "72")
        return

    def test_transmit_rate(self):
        self.check_expression("    Transmit rate (Mbps)   : 72",
                              self.expressions.transmit_rate,
                              self.keys.transmit_rate,
                              "72")
        return

    def test_signal(self):
        self.check_expression("    Signal                 : 99%",
                              self.expressions.signal,
                              self.keys.signal,
                              "99%")
        return
# end class TestNetshWlanExpressions

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    #expressions = netsh.NetshWlanExpressions()
    #keys = netsh.NetshWlanKeys
    #match = expressions.transmit_rate.search("    Transmit rate (Mbps)   : 72")
    #match.groupdict()[keys.transmit_rate]
    output = OutputError(StringIO(""), StringIO("There is no wireless interface on the system.\nHosted network status  : Not available\n"))
    connection = MagicMock()
    connection.netsh.return_value = output
    _netsh = netsh.NetshWlan(connection=connection)
    _netsh.ssid

    
