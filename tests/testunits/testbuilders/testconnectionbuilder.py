# python
from unittest import TestCase

# third-party
from mock import MagicMock
from nose.tools import raises

#tottest
from tottest.connections import adbconnection, sshconnection
from tottest.builders.subbuilders import connectionbuilder
from tottest.commons import errors
ConfigurationError = errors.ConfigurationError


class TestAdbShellConnectionBuilder(TestCase):
    def test_connection(self):
        parameters = MagicMock()
        builder = connectionbuilder.AdbShellConnectionBuilder(parameters)
        connection = builder.connection
        self.assertEqual(adbconnection.ADBShellConnection, type(connection))
        return
# end class TestAdbShellConnectionBuilder


class TestSshConnectionBuilder(TestCase):
    def setUp(self):
        self.section = "DUT"
        self.hostname = "el_hosto"
        self.username = "gimptron3000"
        self.password = "iamthelaw"
        self.parameters = MagicMock()
        self.parameters.section = self.section
        self.parameters.hostname = self.hostname
        self.parameters.username = self.username
        self.parameters.password = self.password
        self.builder = connectionbuilder.SshConnectionBuilder(self.parameters)
        return

    @raises(ConfigurationError)
    def test_hostname_failure(self):
        parameters = MagicMock()
        parameters.hostname = None
        parameters.section = self.section
        builder = connectionbuilder.SshConnectionBuilder(parameters)
        hostname = builder.hostname
        self.assertIsNone(hostname)
        return

    def test_hostname(self):        
        self.assertEqual(self.hostname, self.builder.hostname)
        return

    def test_username(self):
        self.assertEqual(self.username, self.builder.username)
        return

    @raises(ConfigurationError)
    def test_username_fail(self):
        parameters = MagicMock()
        parameters.username = None
        builder = connectionbuilder.SshConnectionBuilder(parameters)
        username = builder.username
        self.assertIsNone(username)
        return

    def test_password(self):
        password = self.builder.password
        self.assertEqual(self.password, password)
        return

    def test_connection(self):
        connection = self.builder.connection
        self.assertIs(sshconnection.SSHConnection, type(connection))
        return
                           
# end class TestSshConnectionBuilder
