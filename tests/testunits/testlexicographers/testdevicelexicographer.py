# python
from unittest import TestCase

#third-party
from mock import MagicMock
from nose.tools import raises

#tottest
from tottest.commons import enumerations
ConnectionTypes = enumerations.ConnectionTypes
from tottest.lexicographers.sublexicographers import devicelexicographer
from tottest.lexicographers.configurationmap import ConfigurationMap
from tottest.commons.errors import ConfigurationError
DeviceLexicographer = devicelexicographer.DeviceLexicographer
DeviceParameters = devicelexicographer.DeviceParameters

from tottest.lexicographers import config_options
ConfigOptions = config_options.ConfigOptions

class TestDeviceLexicographer(TestCase):
    def setUp(self):
        self.parser = MagicMock()
        self.map = ConfigurationMap("dummy")
        self.map._parser = self.parser
        self.section = "NODE1"
        self.test_interface = "wlan0"
        self.operating_system = "linux"
        self.test_ip = "192.168.20.12"
        self.connection_type = ConnectionTypes.ssh
        self.control_ip = "localhost"
        self.login = "joeblow"
        self.password = "passwurt"
        self.paths = "/opt/wifi,/mnt/sdcard"
        self.lexer = devicelexicographer.DeviceLexicographer(parser=self.map, section=self.section)
        return

    def test_operating_system(self):
        self.parser.get.return_value = self.operating_system
        actual = self.lexer.operating_system
        self.assertEqual(self.operating_system, actual)
        self.parser.get.assert_called_with(self.section, ConfigOptions.operating_system_option)
        return

    @raises(ConfigurationError)
    def test_os_missing(self):
        self.parser.get.return_value = None
        self.lexer._operating_system = None
        self.lexer.operating_system
        return
    
    def test_connection_type(self):
        """
        connection_type is a required parameter
        """
        connection_type = self.connection_type
        self.parser.get.return_value = connection_type
        ct = self.lexer.connection_type
        self.parser.get.assert_called_with(self.section, ConfigOptions.connection_option)
        self.assertEqual(connection_type, ct)

    @raises(ConfigurationError)
    def test_connection_type_missing(self):
        # test that this isn't optional
        self.parser.get.return_value = None
        self.lexer._connection_type = None
        self.lexer.connection_type
        return

    def test_test_interface(self):
        expected = self.test_interface
        self.parser.get.return_value = self.test_interface
        actual = self.lexer.test_interface
        self.assertEqual(expected, actual)
        return

    @raises(ConfigurationError)
    def test_test_interface_missing(self):
        self.lexer._test_ip = None
        self.lexer._test_interface = None
        self.parser.get.return_value = None
        self.lexer.test_interface
        return

    def test_test_ip(self):
        """
        test_ip is an optional parameter
        """
        ip = self.test_ip
        self.parser.get.return_value = ip
        tip = self.lexer.test_ip
        self.parser.get.assert_called_with(self.section, ConfigOptions.test_ip_option)
        self.assertEqual(ip, tip)

        # check that it's optional
        self.parser.get.return_value = None
        self.lexer._test_ip = None
        tip = self.lexer.test_ip
        self.assertIsNone(tip)
        return

    def test_control_ip(self):
        """
        control_ip is an optional parameter (for local connections)
        """
        ip = self.control_ip
        values = [ip, None]
    
        self.parser.get.side_effect = values
        cip = self.lexer.control_ip
        self.parser.get.assert_called_with(self.section, ConfigOptions.control_ip_option)
        self.assertEqual(ip, cip)
    
        # test the None case
        cip2 = self.lexer.control_ip
        self.assertEqual(ip, cip2)
        self.lexer._control_ip = None
        cip2 = self.lexer.control_ip
        self.assertIsNone(cip2)
        return
    
    
    def test_login(self):
        """
        login is an optional parameter
        """
        self.parser.get.return_value = self.login
        login = self.lexer.login
        self.parser.get.assert_called_with(self.section, ConfigOptions.login_option)
        self.assertEqual(self.login, login)

        self.lexer._login = None
        self.parser.get.return_value = None
        self.assertIsNone(self.lexer.login)                          
        return
    
    def test_password(self):
        """
        The Password is optional
        """
        self.parser.get.return_value = self.password
        password = self.lexer.password
        self.parser.get.assert_called_with(self.section, ConfigOptions.password_option)
        self.assertEqual(self.password, password)

        self.lexer._password = None
        self.parser.get.return_value = None
        self.assertIsNone(self.lexer.password)
        return
    
    def test_paths(self):
        expected = self.paths.split(",")
        self.parser.get.return_value = self.paths
        paths = self.lexer.paths
        self.parser.get.assert_called_with(self.section, ConfigOptions.paths_option)
        self.assertEqual(expected, paths)

        self.lexer._paths = None
        self.parser.get.return_value = None
        self.assertIsNone(self.lexer.paths)
        return
    
    def test_device_parameters(self):
        """
        """
        s = self.section
        values = {(s,ConfigOptions.operating_system_option):self.operating_system,
                  (s,ConfigOptions.connection_option):self.connection_type,
                  (s, ConfigOptions.test_interface_option):self.test_interface,
                  (s, ConfigOptions.control_ip_option):self.control_ip,
                  (s,ConfigOptions.test_ip_option):self.test_ip,
                  (s, ConfigOptions.login_option): self.login,
                  (s, ConfigOptions.password_option): self.password,
                  (s, ConfigOptions.paths_option):self.paths}
    
        def side_effect(*args):    
            return values[args]
    
        self.parser.get.side_effect=side_effect

        dp = self.lexer.device_parameters
        expected = DeviceParameters(operating_system=self.operating_system,
                                    connection_type=self.connection_type,
                                    test_interface=self.test_interface,
                                    test_ip=self.test_ip,
                                    hostname=self.control_ip,
                                    username=self.login,
                                    password=self.password,
                                    section=self.section,
                                    paths=self.paths.split(","))
        self.assertEqual(expected, dp)
        return
# end class TestDeviceLexicographer
