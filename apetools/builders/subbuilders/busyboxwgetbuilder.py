"""
A module to build a BusyboxWget object.
"""
# python libraries
from collections import namedtuple

# apetools modules
from basetoolbuilder import BaseToolBuilder, Parameters
from apetools.lexicographers.config_options import ConfigOptions
from connectionbuilder import connection_builders, ConnectionBuilderTypes, SSHParameters
from apetools.commands.busyboxwget import BusyboxWget

COLON = ":"

class RotateBuilderEnums(object):
    """
    A holder of Rotate constants
    """
    __slots__ = ()
    angle_velocity = 'angle_velocity'
# end class RotateBuilderEnums

class BusyboxWgetParameters(namedtuple("BusyboxWgetParameters", "target timeout output".split())):
    __slots__ = ()

    def __str__(self):
        return "angle: {0} velocity: {1} clockwise: {2}".format(self.target, self.timeout,
                                                                self.output)
# end class RotateParameters
                           
    
class BusyboxWgetBuilder(BaseToolBuilder):
    """
    A Busybox Wget builder
    """
    def __init__(self, *args, **kwargs):
        super(BusyboxWgetBuilder, self).__init__(*args, **kwargs)
        self._target = None
        self._timeout = None
        self._output = None
        self._connection = None
        return

    @property
    def parameters(self):
        if self._parameters is None:
            self.previous_parameters.append(None)
            self._parameters = self.previous_parameters
        return self._parameters
         
    @property
    def target(self):
        if self._target is None:
            self._target = self.config_map.get(ConfigOptions.busyboxwget_section,
                                               ConfigOptions.target_option)
        return self._target

    @property
    def timeout(self):
        if self._timeout is None:
            self._timeout = self.config_map.get(ConfigOptions.busyboxwget_section,
                                                ConfigOptions.timeout_option,
                                                optional=True,
                                                default=2)
        return self._timeout

    @property
    def output(self):
        if self._output is None:
            self._output = self.config_map.get(ConfigOptions.busyboxwget_section,
                                               ConfigOptions.output_option,
                                               optional=True,
                                               default='/dev/null')
        return self._output

    @property
    def product(self):
        """
        :return: a busybox wget
        """
        if self._product is None:
            self._product = BusyboxWget(connection=self.connection,
                                        target=self.target,
                                        timeout=self.timeout,
                                        output=self.output)
        return self._product


# end class RotateBuilder
    
