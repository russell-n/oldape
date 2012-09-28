"""
A module to build nodes (devices) based on Operating System and connection type
"""

from tottest.baseclass import BaseClass
from connectionbuilder import connection_builders
from devicebuilder import device_builders

class NodeBuilder(BaseClass):
    """
    A class to build a device (node)
    """
    def __init__(self, parameters, lock=None):
        """
        :param:

         - `parameters`: object with attributes needed for device & connection
         - `lock`: A re-entrant lock to pass to the Connection if it will be used in threads
        """
        super(NodeBuilder, self).__init__()
        self.parameters = parameters
        self.lock = lock
        self._connection = None
        self._interface = None
        self._node = None
        self._address = None
        return

    @property
    def address(self):
        """
        :return: the test-interface address (if given)
        """
        if self._address is None:
            try:
                self._address = self.parameters.test_address
            except AttributeError as error:
                self.logger.debug(error)
        return self._address
    
    @property
    def connection(self):
        """
        :return: connection built to match parameter.connection
        """
        if self._connection is None:
            self._connection = connection_builders[self.parameters.connection](self.parameters, self.lock).connection
        return self._connection

    @property
    def interface(self):
        """
        :return: the name of the device's test_interface
        """
        if self._interface is None:
            try:
                self._interface = self.parameters.test_interface
            except AttributeError as error:
                self.logger.debug(error)
        return self._interface

    @property
    def node(self):
        """
        :return: device built to match parameter.operating_system
        """
        if self._node is None:
            self._node = device_builders[self.parameters.operating_system](self.connection,
                                                                           self.interface,
                                                                           self.address).device
        return self._node
# end class NodeBuilder


class NodeBuilderTypes(object):
    __slots__ = ()
    windows = "windows"
    linux = "linux"
# end class NodeBuilderTypes

#node_builders = {NodeBuilderTypes.windows:WindowsNodeBuilder}

