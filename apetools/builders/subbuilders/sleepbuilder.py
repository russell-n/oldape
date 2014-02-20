"""
A module to build a sleep object.
"""
# apetools modules
from basetoolbuilder import BaseToolBuilder, Parameters
from apetools.lexicographers.config_options import ConfigOptions
from apetools.tools.sleep import Sleep
from apetools.commons.errors import ConfigurationError


class SleepConfigurationError(ConfigurationError):
    """
    An error to raise if the user's configuration is wrong
    """
# end class ConfigurationError


class SleepConfigurationEnum(object):
    __slots__ = ()
    time = 'time'
        
class SleepBuilder(BaseToolBuilder):
    """
    A networked oscillator builder
    """
    def __init__(self, *args, **kwargs):
        super(SleepBuilder, self).__init__(*args, **kwargs)
        self.section = ConfigOptions.sleep_section
        return

    @property
    def product(self):
        """
        :return: Sleep object
        """
        if self._product is None:
            time_to_sleep = self.config_map.get_time(self.section,
                                                     ConfigOptions.time_option)
            self._product = Sleep(sleep_time=time_to_sleep)
        return self._product

    @property
    def parameters(self):
        """
        :return: list of named tuples
        """
        if self._parameters is None:
            self._parameters = self.previous_parameters
        return self._parameters
# end class SleepBuilder
