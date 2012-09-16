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

device_parameters = "operating_system connection_type test_interface test_ip hostname username password section paths".split()


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
        self._operating_system = None
        self._connection_type = None
        self._test_interface = None
        self._test_ip = None
        self._control_ip = None
        self._login = None
        self._password = None
        self._paths = None
        self._device_parameters = None
        return

    @property
    def operating_system(self):
        """
        The OS on the device
        
        :rtype: StringType
        :return: the operating system
        """
        if self._operating_system is None:
            self._operating_system = self.parser.get(self.section,
                                                    ConfigOptions.operating_system_option)
        return self._operating_system


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
    def test_interface(self):
        """
        This is required because iperf needs it
        
        :rtype: StringType
        :return: test interface name
        """
        if self._test_interface is None:
            self._test_interface = self.parser.get(self.section,
                                                   ConfigOptions.test_interface_option,
                                                   optional=True)
        return self._test_interface

    @property
    def test_ip(self):
        """
        The preferred parameter is the test interface but if for some reason that doesn't work, use this

        :rtype: String
        :return: test ip address
        """
        if self._test_ip is None:
            self._test_ip = self.parser.get_string(self.section,
                                                   ConfigOptions.test_ip_option,
                                                   optional=True)
        return self._test_ip
    
    @property
    def control_ip(self):
        """
        The preferred parameter is the control interface but if for some reason that doesn't work, use this

        :rtype: String
        :return: control ip address
        """
        if self._control_ip is None:
            self._control_ip = self.parser.get_string(self.section,
                                                   ConfigOptions.control_ip_option,
                                                   optional=True)
        return self._control_ip

    @property
    def login(self):
        """
        This is optional
        
        :rtype: StringType or NoneType
        :return: configured login
        """
        if self._login is None:
            self._login = self.parser.get_string(self.section,
                                                 ConfigOptions.login_option,
                                                 optional=True)
        return self._login

    @property
    def password(self):
        """
        This is optional
        
        :rtype: StringType or NoneType
        :return: configured password
        """
        if self._password is None:
            self._password = self.parser.get_string(self.section,
                                                    ConfigOptions.password_option,
                                                    optional=True)
        return self._password

    @property
    def paths(self):
        """
        :return: A list of paths or None if there were None
        """
        if self._paths is None:
            self._paths = self.parser.get_list(self.section,
                                               ConfigOptions.paths_option,
                                               optional=True)
        return self._paths
    
    @property
    def device_parameters(self):
        """
        :rtype: namedtuple
        :return: the parameters for this device
        """
        if self._device_parameters is None:
            self._device_parameters = DeviceParameters(operating_system=self.operating_system,
                                                       connection_type=self.connection_type,
                                                       test_interface=self.test_interface,
                                                       hostname=self.control_ip,
                                                       test_ip=self.test_ip,
                                                       username=self.login,                                                       
                                                       password=self.password,
                                                       section=self.section,
                                                       paths=self.paths)
            self.logger.debug(str(self._device_parameters))
        return self._device_parameters
# end class DeviceLexicographer
