from unittest import TestCase
from StringIO import StringIO

from mock import MagicMock

from apetools.connections.localconnection import OutputError
from apetools.devices.linuxdevice import LinuxDevice

ifconfig = """
wlan0     Link encap:Ethernet  HWaddr 74:2f:68:e0:e3:33
          inet addr:192.168.2.140  Bcast:192.168.2.255  Mask:255.255.255.0
          inet6 addr: fe80::762f:68ff:fee0:e333/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:32920 errors:0 dropped:0 overruns:0 frame:0
          TX packets:49913 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:3426739 (3.4 MB)  TX bytes:25195468 (25.1 MB)
"""
IP = "192.168.2.140"
MAC = '74:2f:68:e0:e3:33'

iwconfig = """
wlan0     IEEE 802.11bgn  ESSID:"allionstaff"
          Mode:Managed  Frequency:2.437 GHz  Access Point: 18:33:9D:F9:AD:10
          Bit Rate=1 Mb/s   Tx-Power=15 dBm
          Retry  long limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
          Link Quality=67/70  Signal level=-43 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:0   Missed beacon:0
"""

RSSI = "-43"
SSID = "allionstaff"
BSSID = "18:33:9D:F9:AD:10"

class TestLinuxDevice(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.connection.ifconfig.return_value = OutputError(StringIO(ifconfig), "")
        self.connection.iwconfig.return_value = OutputError(StringIO(iwconfig), "")
        self.interface = "wlan0"
        self.device = LinuxDevice(self.connection, interface=self.interface)
        return

    def test_ip_address(self):
        self.assertEqual(IP, self.device.address)
        return

    def test_mac_address(self):
        self.assertEqual(MAC, self.device.mac_address)
        return

    def test_rssi(self):
        self.assertEqual(RSSI, self.device.rssi)
        return

    def test_ssid(self):
        self.assertEqual(SSID, self.device.ssid)
        return

    def test_bssid(self):
        self.assertEqual(BSSID, self.device.bssid)
        return
# end TestLinuxDevice
