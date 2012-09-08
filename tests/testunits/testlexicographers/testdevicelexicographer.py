# python
from unittest import TestCase

#third-party
from mock import MagicMock

#tottest
from tottest.commons import enumerations
ConnectionTypes = enumerations.ConnectionTypes
from tottest.lexicographers.sublexicographers import devicelexicographer
DeviceLexicographer = devicelexicographer.DeviceLexicographer
DeviceParameters = devicelexicographer.DeviceParameters

from tottest.lexicographers import config_options
ConfigOptions = config_options.ConfigOptions

class TestDeviceLexicographer(TestCase):
    def setUp(self):
        self.section = "DUT"
        self.test_ip = "192.168.20.12"
        self.connection_type = ConnectionTypes.ssh
        self.control_ip = "localhost"
        self.login = "joeblow"
        self.password = "passwurt"
        self.paths = "/opt/wifi,/mnt/sdcard"
        return
    
    def test_connection_type(self):
        """
        connection_type is a required parameter
        """
        parser = MagicMock()
        connection_type = self.connection_type
        parser.get.return_value = connection_type
        lexer = devicelexicographer.DeviceLexicographer(parser, self.section)
        ct = lexer.connection_type
        parser.get.assert_called_with(self.section, ConfigOptions.connection_option)
        self.assertEqual(connection_type, ct)
        return

    def test_control_ip(self):
        """
        control_ip is an optional parameter
        """
        ip = self.control_ip
        values = [ip, None]
        parser = MagicMock()

        parser.get_optional.side_effect = values
        lexer = devicelexicographer.DeviceLexicographer(parser, self.section)
        cip = lexer.control_ip
        parser.get_optional.assert_called_with(self.section, ConfigOptions.control_ip_option)
        self.assertEqual(ip, cip)

        # test the None case
        cip2 = lexer.control_ip
        self.assertEqual(ip, cip2)
        lexer._control_ip = None
        cip2 = lexer.control_ip
        self.assertIsNone(cip2)
        return

    def test_test_ip(self):
        """
        test_ip is a required parameter
        """
        ip = self.test_ip
        parser = MagicMock()
        parser.get.return_value = ip
        lexer = devicelexicographer.DeviceLexicographer(parser, self.section)
        tip = lexer.test_ip
        parser.get.assert_called_with(self.section, ConfigOptions.test_ip_option)
        self.assertEqual(ip, tip)
        return

    def test_login(self):
        """
        login is an optional parameter
        """
        parser = MagicMock()
        parser.get_optional.return_value = self.login
        lexer = DeviceLexicographer(parser, self.section)
        login = lexer.login
        parser.get_optional.assert_called_with(self.section, ConfigOptions.login_option)
        self.assertEqual(self.login, login)
        return

    def test_password(self):
        """
        The Password is optional
        """
        parser = MagicMock()
        parser.get_optional.return_value = self.password
        lexer = DeviceLexicographer(parser, self.section)
        password = lexer.password
        parser.get_optional.assert_called_with(self.section, ConfigOptions.password_option)
        self.assertEqual(self.password, password)
        return

    def test_paths(self):
        expected = self.paths.split(",")
        parser = MagicMock()
        parser.get_list.return_value = expected
        lexer = DeviceLexicographer(parser, self.section)
        paths = lexer.paths
        parser.get_list.assert_called_with(self.section, ConfigOptions.paths_option, optional=True)
        self.assertEqual(expected, paths)
        return
    
    def test_device_parameters(self):
        """
        """
        s = self.section
        values = {(s,ConfigOptions.connection_option):self.connection_type,
                  (s,ConfigOptions.test_ip_option):self.test_ip}

        def side_effect(*args):    
            return values[args]

        optionals = {(s, ConfigOptions.login_option): self.login,
                     (s, ConfigOptions.control_ip_option):self.control_ip,
                     (s, ConfigOptions.password_option): self.password}
        def side_effect_optional(*args):
            return optionals[args]

        paths = self.paths.split(",")
        parser = MagicMock()
        parser.get.side_effect=side_effect
        parser.get_optional.side_effect = side_effect_optional
        parser.get_list.return_value = paths
        lexer = DeviceLexicographer(parser, self.section)
        dp = lexer.device_parameters
        expected = DeviceParameters(connection_type=self.connection_type,
                                    test_ip=self.test_ip,
                                    hostname=self.control_ip,
                                    username=self.login,
                                    password=self.password,
                                    section=self.section,
                                    paths=paths)
        self.assertEqual(expected, dp)
        return
# end class TestDeviceLexicographer
