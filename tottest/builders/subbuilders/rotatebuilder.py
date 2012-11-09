"""
A module to build a rotate object.
"""
from basetoolbuilder import BaseToolBuilder, Parameters
from tottest.lexicographers.config_options import ConfigOptions
from connectionbuilder import connection_builders, ConnectionBuilderTypes, SSHParameters
from tottest.commands.rotate import RotateCommand


class RotateBuilderEnums(object):
    """
    A holder of Rotate constants
    """
    __slots__ = ()
    angles = 'angles'
# end class RotateBuilderEnums
    
class RotateBuilder(BaseToolBuilder):
    """
    A Rotator builder
    """
    def __init__(self, *args, **kwargs):
        super(RotateBuilder, self).__init__(*args, **kwargs)
        self._angles = None
        self._connection_parameters = None
        self._connection = None
        return

    @property
    def connection_parameters(self):
        """
        :return: SSHParameters
        """
        if self._connection_parameters is None:
            hostname = self.config_map.get(ConfigOptions.rotate_section,
                                           ConfigOptions.hostname_option)
            username = self.config_map.get(ConfigOptions.rotate_section,
                                           ConfigOptions.username_section)
            password = self.config_map.get(ConfigOptions.rotate_section,
                                           ConfigOptions.username_option,
                                           optional=True)
            self._connection_parameters = SSHParameters(hostname, username, password)

        return self._connection_parameters
    
    @property
    def connection(self):
        """
        :return: ssh-connection to the rotation-master
        """
        if self._connection is None:
            self._connection = connection_builders[ConnectionBuilderTypes.ssh](self.connection_parameters)
        return self._connection

    @property
    def angles(self):
        """
        :return: list of angles
        """
        if self._angles is None:
            self._angles = self.config_map.get_ints(ConfigOptions.rotate_section,
                                                    ConfigOptions.angles_option)
        return self._angles
    
    @property
    def parameters(self):
        """
        :return: list of named-tuple Parameters
        """
        if self._parameters is None:
            self.previous_parameters.append(Parameters(name=RotateBuilderEnums.angles,
                                                       parameter=self.angles))
            self._parameters = self.previous_parameters
        return self._parameters

    @property
    def product(self):
        """
        :return: a rotator
        """
        if self._product is None:
            self._product = RotateCommand(connection=self.connection)
        return self._product
# end class RotateBuilder
    
