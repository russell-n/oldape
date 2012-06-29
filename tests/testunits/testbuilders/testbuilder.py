#python
from unittest import TestCase
from threading import RLock

#third-party
from mock import MagicMock

#tottest
from tottest.builders import builder
from tottest.proletarians import hortator
from tottest.commons import enumerations
ConnectionTypes = enumerations.ConnectionTypes
from tottest.connections import sshconnection
SSHConnection = sshconnection.SSHConnection

class TestBuilder(TestCase):
    def setUp(self):
        self.parameters = MagicMock()
        self.builder = builder.Builder(self.parameters)
        return

    def test_lock(self):
        self.assertIs(type(RLock()), type(self.builder.lock))
        return

    def test_hortator(self):
        #self.builder._operators = MagicMock()
        h = self.builder.hortator
        self.assertIs(hortator.Hortator, type(h))
        return

    def test_tpc_connection(self):
        self.parameters.connection_type = ConnectionTypes.ssh
        self.parameters.hostname = "cw"
        self.parameters.username = "root"
        connection = self.builder.get_tpc_connection(self.parameters)
        self.assertIs(SSHConnection, type(connection))
