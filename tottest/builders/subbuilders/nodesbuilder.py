"""
A module to build id:node-device dictionaries
"""

from tottest.lexicographers.config_options import ConfigOptions
from tottest.devices.dummydevice import DummyDevice

class NodeTypes(object):
    __slots__ = ()
    dummy = "dummy"
# end class NodeTypes

class NodesBuilder(object):
    """
    A generic builder of id:device dictionaries
    """
    def __init__(self, builder, config_map):
        """
        :param:

         - `builder`: the master builder
         - `config_map`: A configuration map to get the parameters from
        """
        self.builder = builder
        self.config_map = config_map
        self._nodes = None
        return

    @property
    def nodes(self):
        """
        :return: dictionary of id:device nodes
        """
        if self._nodes is None:
            nodes = self.config_map.options(ConfigOptions.nodes_section)
            if nodes is None:
                self._nodes = {NodeTypes.dummy:DummyDevice()}
        return self._nodes
# end class NodesBuilder
