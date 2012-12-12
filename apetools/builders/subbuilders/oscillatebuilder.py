"""
A module to build a rotate object.
"""
# apetools modules
from basetoolbuilder import BaseToolBuilder
from apetools.lexicographers.config_options import ConfigOptions

from apetools.connections.sshconnection import SSHConnection
from apetools.commands.oscillate import Oscillate, OscillateStop

from apetools.commons.errors import ConfigurationError

class OscillatorConfigurationError(ConfigurationError):
    """
    An error to raise if the user's configuration is wrong
    """
# end class OscillatorConfigurationError


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
        self._output = None
        self._arguments = None
        self._block = None
        self.section = ConfigOptions.oscillate_section
        return

    @property
    def block(self):
        """
        :return: Boolean on whether to block and wait for rotation start
        """
        if self._block is None:
            self._block = self.config_map.get_boolean(self.section,
                                                      ConfigOptions.block_option,
                                                      default=False,
                                                      optional=True)
        return self._block

    def get_option(self, option, optional=False):
        """
        :param:

         - `option`: the option name in the config file
         - `optional`: if True, return None for missing option

        :return: the option value 
        """        
        return self.config_map.get(self.section, option, optional=optional)

    @property
    def output(self):
        """
        :return: file to output angles to
        """
        if self._output is None:
            self._output = self.master.storage.open("oscillate.log", 'logs')
        return self._output

    @property
    def arguments(self):
        """
        :return: string of arguments for the oscillate command
        """
        if self._arguments is None:
            arguments = {}
            section = ConfigOptions.oscillate_section
            for option in (ConfigOptions.start_option,
                           ConfigOptions.arc_option,
                           ConfigOptions.timeout_option,
                           ConfigOptions.noise_start_option,
                           ConfigOptions.noise_end_option,            
                           ConfigOptions.port_option):
                value = self.config_map.get(section, option,optional=True)
                if value is not None:
                    arguments[option] = value
            self._arguments = " ".join(["--{0} {1}".format(key, value) for key,value in arguments.iteritems()])
        return self._arguments
    
    
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
            self._product = Oscillate(connection=self.connection,
                                      output=self.output,
                                      arguments=self.arguments,
                                      block=self.block)
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

class OscillateStopBuilder(BaseToolBuilder):
    """
    A networked oscillator stopper builder
    """
    def __init__(self, *args, **kwargs):
        super(OscillateStopBuilder, self).__init__(*args, **kwargs)
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
            self._product = OscillateStop(connection=self.connection)
        return self._product

    @property
    def parameters(self):
        """
        :return: list of named tuples
        """
        if self._parameters is None:
            self._parameters = self.previous_parameters
        return self._parameters
# end class OscillateStopBuilder
