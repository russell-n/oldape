"""
A module to build a traffic PC device
"""

from apetools.lexicographers.config_options import ConfigOptions
from apetools.builders.subbuilders.connectionbuilder import connection_builders
from apetools.devices.basedevice import BaseDeviceEnum
from nodebuilder import NodeBuilder


class TpcDeviceBuilder(object):
    """
    A class to build the TPC device
    """
    def __init__(self, config_map):
        """
        :param:

         - `config_map`: a map to get the configurations
        """
        self.config_map = config_map
        self._device = None
        self._connection = None
        self._parameters = None
        return

    @property
    def parameters(self):
        """
        :return: namedtuple of parameters for the device
        """
        if self._parameters is None:
            tpc = self.config_map.options(ConfigOptions.traffic_pc_section)[0]
            self._parameters = self.config_map.get_namedtuple(ConfigOptions.traffic_pc_section,
                                                            tpc)
        return self._parameters

    @property
    def connection(self):
        """
        :return: connection to the TPC
        """
        if self._connection is None:
            self._connection = connection_builders[self._parameters.connection](self._parameters)
        return self._connection

    @property
    def device(self):
        """
        :return: device for the TPC
        """
        if self._device is None:
            self._device = NodeBuilder(parameters=self.parameters,
                                       role=BaseDeviceEnum.tpc).node
        return self._device
# end class TpcDeviceBuilder
