"""
A module to build id:node-device dictionaries
"""

#python
from string import lower

#tottest
from tottest.baseclass import BaseClass
from tottest.lexicographers.config_options import ConfigOptions
from tottest.devices.dummydevice import DummyDevice
from nodebuilder import NodeBuilder

class NodeTypes(object):
    __slots__ = ()
    dummy = "dummy"
# end class NodeTypes

class NodesBuilder(BaseClass):
    """
    A generic builder of id:device dictionaries
    """
    def __init__(self, builder, config_map):
        """
        :param:

         - `builder`: the master builder
         - `config_map`: A configuration map to get the parameters from
        """
        super(NodesBuilder, self).__init__()
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
            self._nodes = {}
            try:
                config_tuples = [self.config_map.get_namedtuple(ConfigOptions.nodes_section,node, converter=lower)
                               for node in nodes]
                node_tuples = dict(zip(nodes, config_tuples))
                for node, parameters in node_tuples.items():
                    self._nodes[node] = NodeBuilder(parameters, self.builder.lock).node
            except TypeError as error:
                self.logger.debug(error)
                self._nodes[NodeTypes.dummy] = DummyDevice()        
        return self._nodes
# end class NodesBuilder
