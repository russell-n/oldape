
# python libraries
from collections import namedtuple

# apetools modules
from basetoolbuilder import BaseToolBuilder, Parameters
from apetools.lexicographers.config_options import ConfigOptions
from connectionbuilder import connection_builders, ConnectionBuilderTypes, SSHParameters
from apetools.commands.rotate import RotateCommand


COLON = ":"

class RotateBuilderEnums(object):
    """
    A holder of Rotate constants
    """
    __slots__ = ()
    angle_velocity = 'angle_velocity'
# end class RotateBuilderEnums


class RotateParameters(namedtuple("RotateParameters", "angle velocity clockwise".split())):
    __slots__ = ()

    def __str__(self):
        return "angle: {0} velocity: {1} clockwise: {2}".format(self.angle, self.velocity,
                                                                self.clockwise)
# end class RotateParameters


class RotateBuilder(BaseToolBuilder):
    """
    A Rotator builder
    """
    def __init__(self, *args, **kwargs):
        super(RotateBuilder, self).__init__(*args, **kwargs)
        self._angles = None
        self._velocities = None
        self._connections_parameters = None
        self._connections = None
        return

    @property
    def connections_parameters(self):
        """
        :return: list of SSHParameters
        """
        if self._connections_parameters is None:
            section = ConfigOptions.rotate_section
            nodes = (option for option in self.config_map.options(section)
                     if option.startswith('node'))
            node_kwargs = (self.config_map.get_dictionary(section, node) for node in nodes)
            self._connections_parameters = [SSHParameters(**kwargs) for kwargs in node_kwargs]
        return self._connections_parameters
    
    @property
    def connections(self):
        """
        :return: list of ssh-connections to the rotation-master
        """
        if self._connections is None:
            self._connections = [connection_builders[ConnectionBuilderTypes.ssh](parameters).connection for
                                 parameters in self.connections_parameters]
        return self._connections

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
                                                   velocity=True)
        return self._velocities                                                        
    
    @property
    def parameters(self):
        """
        :return: list of named-tuple Parameters
        """
        if self._parameters is None:
            parameters = []
            values = self.config_map.get_list(ConfigOptions.rotate_section,
                                                    ConfigOptions.angles_option)
            for list_index, item in enumerate(values):
                if COLON in item:
                    angle, velocity = item.split(COLON)
                else:
                    angle, velocity = item, 0

                    # check the direction
                clockwise = angle.startswith('-') 
                parameters.append(RotateParameters(angle.lstrip('-'), velocity,
                                                   clockwise))

            self.previous_parameters.append(Parameters(name=RotateBuilderEnums.angle_velocity,
                                                       parameters=parameters))
            self._parameters = self.previous_parameters
        return self._parameters

    @property
    def product(self):
        """
        :return: a RotateCommand
        """
        if self._product is None:
            self._product = RotateCommand(connections=self.connections)
        return self._product

# end class RotateBuilder
