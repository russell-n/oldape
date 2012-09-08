from unittest import TestCase
from StringIO import StringIO

from mock import MagicMock
from tottest.tools import wifitool

import wpa_cli_status, iw_link, wpa_cli_interface_list


class WifiToolTest(TestCase):
    def setUp(self):
        self.tool = wifitool.WifiToolAdb()
        self.connection = MagicMock()
        self.tool._connection = self.connection
        return

    def test_status(self):
        output = StringIO(wpa_cli_status.output)
        error = StringIO('')
        self.connection.wpa_cli.return_value = output, error
        self.assertEqual(wpa_cli_status.output, self.tool.status_command.status)
        return

    def test_rssi(self):
        output = StringIO(iw_link.output)
        error = StringIO('')
        self.connection.iw.return_value = output, error
        self.tool.rssi_command._interface = "wlan0"
        rssi  = self.tool.rssi_command.rssi
        self.connection.iw.assert_called_with("dev wlan0 link")
        self.assertEqual(iw_link.rssi, rssi)
        return


    def test_ip(self):
        output = StringIO(wpa_cli_status.output)
        error = StringIO('')
        self.connection.wpa_cli.return_value = output, error

        self.assertEqual(wpa_cli_status.ip, self.tool.ip_command.ip_address)
        return

    def test_interface(self):
        output = StringIO(wpa_cli_interface_list.output)
        error = StringIO('')
        self.connection.wpa_cli.return_value = output, error

        self.assertEqual(wpa_cli_interface_list.interface,
                         self.tool.interface_command.interface)
        return

    def test_mac(self):
        output = StringIO(wpa_cli_status.output)
        error = StringIO('')
        self.connection.wpa_cli.return_value = output, error
        self.assertEqual(wpa_cli_status.mac, self.tool.mac_command.mac_address)
        return
        
    def test_ssid(self):
        output = StringIO(wpa_cli_status.output)
        error = StringIO('')
        self.connection.wpa_cli.return_value = output, error
        self.assertEqual(wpa_cli_status.ssid, self.tool.ssid_command.ssid)
        return
