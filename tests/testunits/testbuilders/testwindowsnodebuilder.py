from unittest import TestCase

from mock import MagicMock

from apetools.builders.subbuilders.nodebuilder import WindowsNodeBuilder
from apetools.connections.sshconnection import SSHConnection
from apetools.devices.windowsdevice import WindowsDevice

class TestWindowsNodeBuilder(TestCase):
    def setUp(self):
        self.parameters = MagicMock()
        self.parameters.connection = "ssh"
        self.parameters.operating_system = "windows"
        self.builder = WindowsNodeBuilder(self.parameters)
        return

    def test_connection(self):
        self.assertIsInstance(self.builder.connection, SSHConnection)
        return

    def test_node(self):
        self.assertIsInstance(self.builder.node, WindowsDevice)
        self.assertIsInstance(self.builder.node.connection, SSHConnection)
        return
# end class TestWindowsNodeBuilder
