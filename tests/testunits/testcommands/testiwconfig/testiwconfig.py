from unittest import TestCase
from StringIO import StringIO

from mock import MagicMock
from nose.tools import raises

from tottest.commands.iwconfig import Iwconfig
from tottest.connections.localconnection import OutputError
from tottest.commons.errors import CommandError

OUTPUT = """
wlan0     IEEE 802.11bgn  ESSID:"allionstaff"
          Mode:Managed  Frequency:2.437 GHz  Access Point: 18:33:9D:F9:AD:10
          Bit Rate=1 Mb/s   Tx-Power=15 dBm
          Retry  long limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
          Link Quality=67/70  Signal level=-43 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:2  Invalid misc:0   Missed beacon:0
"""

BAD_INTERFACE = """
eth3      No such device
"""


class TestIwconfig(TestCase):
    def setUp(self):
        self.interface = "wlan0"
        self.connection = MagicMock()
        self.connection.iwconfig.return_value = OutputError(StringIO(OUTPUT), "")
        self.command = Iwconfig(connection=self.connection, interface=self.interface)
        
        return

    def test_ssid(self):
        expected = "allionstaff"
        actual = self.command.ssid
        self.assertEqual(expected, actual)
        self.connection.iwconfig.assert_called_with(self.interface)
        return

    def test_bssid(self):
        expected = "18:33:9D:F9:AD:10"
        actual = self.command.bssid
        self.assertEqual(expected, actual)
        return

    def test_rssi(self):
        expected = "-43"
        actual = self.command.rssi
        self.assertEqual(expected, actual)
        return

    @raises(CommandError)
    def test_no_interface(self):
        connection = MagicMock()
        connection.iwconfig.return_value = OutputError(StringIO(BAD_INTERFACE), "")
        command = Iwconfig(connection = connection, interface="eth3")
        rssi = command.rssi
        self.assertEqual(rssi, command.not_available)
        return
# end class TestIwconfig
