from unittest import TestCase
from mock import MagicMock
from StringIO import StringIO

from tottest.commands.winrssi import WinRssi, NA
from tottest.commons.errors import CommandError
from tottest.connections.localconnection import OutputError

class TestWinRssi(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.command = WinRssi(self.connection)
        return

    def test_rssi(self):
        expected = "-42"
        self.connection.rssi.return_value = OutputError(StringIO("-42\n"),"")
        actual = self.command()
        self.assertEqual(expected, actual)
        return

    def test_interface_disabled(self):
        self.connection.rssi.return_value = OutputError(StringIO("Unable to find the wireless interface. Is it enabled?\n"),"")
        self.assertRaises(CommandError, self.command)
        return

    def test_disconnected(self):
        self.connection.rssi.return_value = OutputError(StringIO("The group or resource is not in the correct state to perform the requested operation. Is it connected to an AP?\n"),
                                                        "")
        self.assertRaises(CommandError, self.command)
        return

    def test_na(self):
        expected = NA
        self.connection.rssi.return_value = OutputError(StringIO("umma gumma"), "")
        actual = self.command()
        self.assertEqual(expected, actual)
# end class TestWinRssi
