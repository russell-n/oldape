"""
A Device Lexicographer is a sub-lexicographer that tries to get all possible device parameters.
It defers the checking of parameters to the Builders who are assumed to know the objects better.
"""

#python
from collections import namedtuple

#tottest
from tottest.lexicographers import config_options
ConfigOptions = config_options.ConfigOptions
from tottest.baseclass import BaseClass

device_parameters = "connection_type test_ip hostname username password section".split()


class DeviceParameters(namedtuple("DeviceParameters", device_parameters)):
    """
    Parameters needed to configure device connections
    """
    __slots__ = ()
    def __str__(self):
        return ','.join(("{f}:{v}".format(f=f, v=getattr(self, f))
                         for f in self._fields))
# end DeviceParameters


class DeviceLexicographer(BaseClass):
    """
    DeviceLexicographer builds Device Parameters
    """
    def __init__(self, parser, section):
        """
        :param:

         - `parser`: a Configuration Map
         - `section`: name of the configuration section
        """
        super(DeviceLexicographer, self).__init__()
        self.parser = parser
        self.section = section
        self._connection_type = None
        self._control_ip = None
        self._test_ip = None
        self._login = None
        self._password = None
        self._device_parameters = None
        return

    @property
    def connection_type(self):
        """
        This is required to determine the correct builder
        :rtype: StringType
        :return: the connection type
        """
        if self._connection_type is None:
            self._connection_type = self.parser.get(self.section,
                                                    ConfigOptions.connection_option)
        return self._connection_type

    @property
    def control_ip(self):
        """
        This is optional since ADBLocal and Local don't need it
        
        :rtype: StringType or NoneType
        :return: control ip in config
        """
        if self._control_ip is None:
            self._control_ip = self.parser.get_optional(self.section,
                                                        ConfigOptions.control_ip_option)
        return self._control_ip

    @property
    def test_ip(self):
        """
        This is required because iperf needs it (for now)
        
        :rtype: StringType
        :return: test ip address for the device
        """
        if self._test_ip is None:
            self._test_ip = self.parser.get(self.section,
                                     ConfigOptions.test_ip_option)
        return self._test_ip

    @property
    def login(self):
        """
        This is optional
        
        :rtype: StringType or NoneType
        :return: configured login
        """
        if self._login is None:
            self._login = self.parser.get_optional(self.section,
                                                   ConfigOptions.login_option)
        return self._login

    @property
    def password(self):
        """
        This is optional
        
        :rtype: StringType or NoneType
        :return: configured password
        """
        if self._password is None:
            self._password = self.parser.get_optional(self.section,
                                                      ConfigOptions.password_option)
        return self._password
    
    @property
    def device_parameters(self):
        """
        :rtype: namedtuple
        :return: the parameters for this device
        """
        if self._device_parameters is None:
            self._device_parameters = DeviceParameters(connection_type=self.connection_type,
                                                       hostname=self.control_ip,
                                                       test_ip=self.test_ip,
                                                       username=self.login,
                                                       password=self.password,
                                                       section=self.section)
            self.logger.debug(str(self._device_parameters))
        return self._device_parameters
# end class DeviceLexicographer
