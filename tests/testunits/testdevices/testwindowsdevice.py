from unittest import TestCase

from mock import MagicMock

from tottest.devices import windowsdevice

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


class TestWindowsDevice(TestCase):
    def setUp(self):
        self.wmic = MagicMock()
        self.netsh = MagicMock()
        self.rssi = MagicMock()
        self.connection = MagicMock()
        self.device = windowsdevice.WindowsDevice(connection=self.connection)
        self.device._wifi_control = self.wmic
        self.device._wifi_query = self.netsh
        self.device._rssi_query = self.rssi
        return

    def test_disable_wifi(self):
        self.device.disable_wifi()
        self.wmic.disable_wifi.assert_called_with()
        return

    def test_enable_wifi(self):
        self.device.enable_wifi()
        self.wmic.enable_wifi.assert_called_with()
        return

    def test_rssi(self):
        expected = "-32"
        self.rssi.return_value = expected
        actual = self.device.rssi
        self.rssi.assert_called_with()
        self.assertEqual(expected, actual)        
        return

    def test_get_wifi_info(self):
        rssi = "-89"
        self.rssi.return_value = rssi
        self.netsh.output = OUTPUT.split("\n")
        actual = self.device.wifi_info
        #self.netsh.output.assert_called_with()
        print self.rssi.mock_calls
        self.rssi.assert_called_with()
        expected = OUTPUT  + "\nrssi: {0} dbm".format(rssi)
        self.assertEqual(expected, actual)
        return
#  class TestWindowsDevice
