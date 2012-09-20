"""
A module to build nodes (devices) based on Operating System and connection type
"""

from tottest.baseclass import BaseClass
from connectionbuilder import connection_builders
from devicebuilder import device_builders

class WindowsNodeBuilder(BaseClass):
    """
    A class to build a Windows device
    """
    def __init__(self, parameters, lock=None):
        """
        :param:

         - `parameters`: object with attributes needed for device & connection
         - `lock`: A re-entrant lock to pass to the Connection if it will be used in threads
        """
        self.parameters = parameters
        self.lock = lock
        self._connection = None
        self._node = None
        return

    @property
    def connection(self):
        """
        :return: connection built to match parameter.connection
        """
        if self._connection is None:
            self._connection = connection_builders[self.parameters.connection](self.parameters, self.lock).connection
        return self._connection

    @property
    def node(self):
        """
        :return: device built to match parameter.operating_system
        """
        if self._node is None:
            self._node = device_builders[self.parameters.operating_system](self.connection).device
        return self._node
# end class WindowsNodeBuilder

class NodeBuilderTypes(object):
    __slots__ = ()
    windows = "windows"
# end class NodeBuilderTypes

node_builders = {NodeBuilderTypes.windows:WindowsNodeBuilder}

