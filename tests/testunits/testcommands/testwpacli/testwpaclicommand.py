from unittest import TestCase
from StringIO import StringIO

from nose.tools import raises
from mock import MagicMock

from apetools.commands import wpacli
from apetools.commons import errors

CommandError = errors.CommandError

import wpa_cli_error, wpa_cli_interface_list, wpa_cli_status

class WpaCliCommandTest(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.command = wpacli.WpaCliCommand(connection=self.connection)
        return

    def test_interface(self):
        output = StringIO(wpa_cli_interface_list.output)
        error = StringIO('')
        self.connection.wpa_cli.return_value = output, error
        self.assertEqual(wpa_cli_interface_list.interface, self.command.interface)
        self.connection.wpa_cli.assert_called_with("interface_list")
        return

    def test_ip(self):
        output = StringIO(wpa_cli_status.output)
        error = StringIO('')
        self.connection.wpa_cli.return_value = output, error
        self.assertEqual(wpa_cli_status.ip, self.command.ip_address)
        self.connection.wpa_cli.assert_called_with("status")
        return

    def test_mac(self):
        output = StringIO(wpa_cli_status.output)
        error = StringIO('')
        self.connection.wpa_cli.return_value = output, error
        self.assertEqual(wpa_cli_status.mac, self.command.mac_address)
        self.connection.wpa_cli.assert_called_with("status")
        return

    def test_ssid(self):
        output = StringIO(wpa_cli_status.output)
        error = StringIO('')
        self.connection.wpa_cli.return_value = output, error
        self.assertEqual(wpa_cli_status.ssid, self.command.ssid)
        self.connection.wpa_cli.assert_called_with('status')
        return
    
    def test_status(self):
        output = StringIO(wpa_cli_status.output)
        error = StringIO('')
        self.connection.wpa_cli.return_value = output, error
        self.assertEqual(wpa_cli_status.output, self.command.status)
        self.connection.wpa_cli.assert_called_with("status")
        
        
    @raises(CommandError)
    def test_error(self):
        output = StringIO('')
        error = StringIO(wpa_cli_error.output)
        self.connection.wpa_cli.return_value = output, error
        self.assertEqual(None, self.command.mac_address)
        
# end class IwCommandTest
