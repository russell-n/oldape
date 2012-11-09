"""
A module to build time-to-recovery tools
"""

from basetoolbuilder import BaseToolBuilder, Parameters
from tottest.tools.timetorecovery import TimeToRecovery
from tottest.lexicographers.config_options import ConfigOptions

class TimeToRecoveryBuilderEnum(object):
    __slots__ = ()
    nodes = 'nodes'
    target = 'target'
    timeout = "timeout"
    threshold = "threshold"
# end class TimeToRecoveryBuilderEnum


class TimeToRecoveryBuilder(BaseToolBuilder):
    """
    A builder of TTR Objects
    """
    def __init__(self, *args, **kwargs):
        super(TimeToRecoveryBuilder, self).__init__(*args, **kwargs)
        self._target = None
        self._ttr = None
        self._timeout = None
        self._threshold = None
        return

    @property
    def section(self):
        """
        :return: the name of the section in the config_file
        """
        if self._section is None:
            self._section = ConfigOptions.time_to_recovery_section
        return self._section
    
    @property
    def timeout(self):
        """
        :return: the total time to try and ping
        """
        if self._timeout is None:
            self._timeout = self.config_map.get_int(ConfigOptions.time_to_recovery_section,
                                                    ConfigOptions.timeout_option,
                                                    optional=True,
                                                    default=300)
        return self._timeout

    @property
    def threshold(self):
        """
        :return: the number of consecutive pings to count as a recovery sign
        """
        if self._threshold is None:
            self._threshold = self.config_map.get_int(ConfigOptions.time_to_recovery_section,
                                                      ConfigOptions.threshold_option,
                                                      optional=True,
                                                      default=5)
        return self._threshold
    

    @property
    def target(self):
        """
        :return: target from the config file
        """
        if self._target is None:
            self._target = self.master.tpc_device.address
        return self._target
    
    @property
    def ttr(self):
        """
        :return: A time to recovery object
        """
        if self._ttr is None:
            self._ttr = TimeToRecovery(nodes=self.master.nodes)
        return self._ttr

    @property
    def product(self):
        """
        :return: a TTR
        """
        if self._product is None:
            self._product = TimeToRecovery(self.master.nodes)
        return self._product

    @property
    def parameters(self):
        """
        :return: namedtuple with `name` and `parameters` attribute
        """
        if self._parameters is None:
            self.add_parameter(TimeToRecoveryBuilderEnum.nodes,
                               self.master.nodes.keys())

            self.add_parameter(TimeToRecoveryBuilderEnum.target,
                               [self.target])
            self.add_parameter(TimeToRecoveryBuilderEnum.threshold,
                               [self.threshold])
            self.add_parameter(TimeToRecoveryBuilderEnum.timeout,
                               [self.timeout])
            self._parameters = self.previous_parameters
        return self._parameters

    def add_parameter(self, name, value):
        """
        :param:

         - `name`: the name of the parameter to add
         - `value`: the value of the parameter to add

        :postcondition: Parameters(name, value) in self.previous_parameters
        """
        if not any([p.name == name for p in self.previous_parameters]):
            self.previous_parameters.append(Parameters(name=name, parameters=value))
        return
# end TimeToRecoveryBuilder
