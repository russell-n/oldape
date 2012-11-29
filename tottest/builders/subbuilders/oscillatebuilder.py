"""
A module to build a rotate object.
"""
# python libraries
from collections import namedtuple

# tottest modules
from basetoolbuilder import BaseToolBuilder
from tottest.lexicographers.config_options import ConfigOptions

from tottest.connections.sshconnection import SSHConnection
from tottest.commands.oscillator import Oscillator

from tottest.commons.errors import ConfigurationError

class OscillatorConfigurationError(ConfigurationError):
    """
    An error to raise if the user's configuration is wrong
    """
# end class OscillatorConfigurationError

class PowerOnBuilderEnum(object):
    """
    A holder of Synaxxx constants
    """
    __slots__ = ()
    id_switch = "id_switch"
# end class PowerOnBuilderEnums

class OscillatorParameters(namedtuple("PowerOnParameters", "identifier switch".split())):
    __slots__ = ()

    def __str__(self):
        return "identifier: {0} switch: {1}".format(self.identifier,
                                                    self.switch)
# end class PowerOnParameters
                           
    
class OscillateBuilder(BaseToolBuilder):
    """
    A networked oscillator builder
    """
    def __init__(self, *args, **kwargs):
        super(OscillateBuilder, self).__init__(*args, **kwargs)
        self._connection = None
        self._hostname = None
        self._username = None
        self._password = None
        self.section = ConfigOptions.oscillate_section
        return

    def get_option(self, option, optional=False):
        """
        :param:

         - `option`: the option name in the config file
         - `optional`: if True, return None for missing option

        :return: the option value 
        """        
        return self.config_map.get(self.section, option, optional=optional)

    @property
    def hostname(self):
        """
        :return: the address to the oscillator
        """
        if self._hostname is None:
            self._hostname = self.get_option(ConfigOptions.hostname_option)
        return self._hostname

    @property
    def username(self):
        """
        :return: the username to log in to the oscillator
        """
        if self._username is None:
            self._username = self.get_option(ConfigOptions.username_option)
        return self._username

    @property
    def password(self):
        """
        :return: the password to log in to the oscillator
        """
        if  self._password is None:
            self._password = self.get_option(ConfigOptions.password_option,
                                             True)
        return self._password

    @property
    def connection(self):
        """
        :return: sshconnection to the oscillator
        """
        if self._connection is None:
            self._connection = SSHConnection(self.hostname,
                                             self.username,
                                             self.password)
        return self._connection
    
    @property
    def product(self):
        """
        :return: PowerOn object
        """
        if self._product is None:
            self._product = Oscillator(self.connection)
        return self._product

    @property
    def parameters(self):
        """
        :return: list of named tuples
        """
        if self._parameters is None:
            self._parameters = self.previous_parameters
        return self._parameters
# end class PowerOnBuilder            
