"""
A module to build a rotate object.
"""
from basetoolbuilder import BaseToolBuilder, Parameters
from tottest.lexicographers.config_options import ConfigOptions
from connectionbuilder import connection_builders, ConnectionBuilderTypes, SSHParameters
from tottest.commands.rotate import RotateCommand

COLON = ":"

class RotateBuilderEnums(object):
    """
    A holder of Rotate constants
    """
    __slots__ = ()
    angles = 'angles'
    velocities = 'velocities'
# end class RotateBuilderEnums
    
class RotateBuilder(BaseToolBuilder):
    """
    A Rotator builder
    """
    def __init__(self, *args, **kwargs):
        super(RotateBuilder, self).__init__(*args, **kwargs)
        self._angles = None
        self._velocities = None
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
                                           ConfigOptions.username_option)
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
            self._connection = connection_builders[ConnectionBuilderTypes.ssh](self.connection_parameters).connection
            assert self._connection.__class__.__name__ == "SSHConnection", self._connection.__class__.__name__
        return self._connection

    @property
    def angles(self):
        """
        :return: list of angles
        """
        if self._angles is None:
            self._angles = self.get_parameters()
        return self._angles

    @property
    def velocities(self):
        """
        :return: list of velocities
        """
        if self._velocities is None:
            self._velocities = self.get_parameters(parameter_index=1,
                                                   pad=True)
        return self._velocities                                                        
    
    @property
    def parameters(self):
        """
        :return: list of named-tuple Parameters
        """
        if self._parameters is None:
            self.previous_parameters.append(Parameters(name=RotateBuilderEnums.angles,
                                                       parameters=self.angles))
            self.previous_parameters.append(Parameters(name=RotateBuilderEnums.velocities,
                                                       parameters=self.velocities))
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

    def get_parameters(self, parameter_index=0, pad=False):
        """
        :param:

         - `parameter_index`: index of the item wanted if there is a velocity in the parameter
         - `pad`: if true, put a 0 in the list when there's no velocity

        :return: list of integer parameters
        """
        parameters = self.config_map.get_list(ConfigOptions.rotate_section,
                                                    ConfigOptions.angles_option)
        for list_index, item in enumerate(parameters):
            if COLON in item:
                value = parameters[list_index].split(COLON)[parameter_index]
            else:
                value = 0
            parameters[list_index] = value                
        return parameters
# end class RotateBuilder
    
