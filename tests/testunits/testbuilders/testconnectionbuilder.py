# python
from unittest import TestCase
from collections import namedtuple

# third-party
from mock import MagicMock
from nose.tools import raises

#tottest
from tottest.connections import adbconnection, sshconnection
from tottest.builders.subbuilders import connectionbuilder
from tottest.commons import errors
ConfigurationError = errors.ConfigurationError


noattr = namedtuple("NoAttr", "a b c".split())
test_no_attr = noattr(None, None, None)

class TestAdbShellConnectionBuilder(TestCase):
    def test_connection(self):
        parameters = MagicMock()
        builder = connectionbuilder.AdbShellConnectionBuilder(parameters)
        connection = builder.connection
        self.assertEqual(adbconnection.ADBShellConnection, type(connection))
        return
# end class TestAdbShellConnectionBuilder


class TestSSHConnectionBuilder(TestCase):
    def setUp(self):
        self.section = "DUT"
        self.hostname = "el_hosto"
        self.username = "gimptron3000"
        self.password = "iamthelaw"
        self.operating_system = "windows"
        self.parameters = MagicMock()
        self.lock = MagicMock()
        self.parameters.section = self.section
        self.parameters.hostname = self.hostname
        self.parameters.username = self.username
        self.parameters.password = self.password
        self.parameters.operating_system = self.operating_system
        self.builder = connectionbuilder.SSHConnectionBuilder(self.parameters, self.lock)
        return

    @raises(ConfigurationError)
    def test_hostname_failure(self):
        parameters = test_no_attr
        builder = connectionbuilder.SSHConnectionBuilder(parameters, self.lock)
        hostname = builder.hostname
        return

    def test_hostname(self):        
        self.assertEqual(self.hostname, self.builder.hostname)
        self.assertEqual(self.hostname, self.builder.connection.hostname)
        return

    def test_username(self):
        self.assertEqual(self.username, self.builder.username)
        self.assertEqual(self.username, self.builder.connection.username)
        return

    @raises(ConfigurationError)
    def test_username_fail(self):
        parameters = test_no_attr
        builder = connectionbuilder.SSHConnectionBuilder(parameters, self.lock)
        username = builder.username
        return

    def test_password(self):
        password = self.builder.password
        self.assertEqual(self.password, password)
        self.assertEqual(self.password, self.builder.connection.password)
        return

    def test_connection(self):
        connection = self.builder.connection
        self.assertIs(sshconnection.SSHConnection, type(connection))
        return

    def test_operating_system(self):
        os = self.builder.operating_system
        self.assertEqual(self.operating_system , os)
        self.assertEqual(self.builder.connection.operating_system, os)
        return
# end class TestSshConnectionBuilder
