from unittest import TestCase
from StringIO import StringIO

from nose.tools import raises
from mock import MagicMock

from apetools.commands import iwcommand
from apetools.commons import errors

CommandError = errors.CommandError

import iw_dev, iw_link, iw_error

class IwCommandTest(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.command = iwcommand.IwCommand(connection=self.connection)
        return

    def test_interface(self):
        output = StringIO(iw_dev.output)
        error = StringIO('')
        self.connection.iw.return_value = output, error
        self.assertEqual(iw_dev.interface, self.command.interface)
        self.connection.iw.assert_called_with("dev")
        return

    def test_rssi(self):
        output = StringIO(iw_link.output)
        error = StringIO('')
        self.command._interface = iw_dev.interface
        self.connection.iw.return_value = output, error
        self.assertEqual(iw_link.rssi, self.command.rssi)
        self.connection.iw.assert_called_with("dev {iface} link".format(iface=iw_dev.interface))
        return

    @raises(CommandError)
    def test_error(self):
        output = StringIO('')
        error = StringIO(iw_error.output)
        self.connection.iw.return_value = output, error
        self.assertEqual(None, self.command.rssi)
        
# end class IwCommandTest
