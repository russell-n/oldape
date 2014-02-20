
from apetools.baseclass import BaseClass
from apetools.commons.errors import ConfigurationError
from apetools.devices.basedevice import BaseDeviceEnum
from connectionbuilder import connection_builders
from devicebuilder import device_builders
from apetools.lexicographers.config_options import ConfigOptions


class NodeBuilder(BaseClass):
    """
    A class to build a device (node)
    """
    def __init__(self, parameters, role=None):
        """
        NodeBuilder Constructor
        :param:

         - `parameters`: object with attributes needed for device & connection
         - `role`: tpc or node
        """
        super(NodeBuilder, self).__init__()
        self.parameters = parameters
        self._role = role
        self._connection = None
        self._interface = None
        self._node = None
        self._address = None
        return

    @property
    def role(self):
        """
        Sets the role to BaseDeviceEnum.node
        
        :return: the device role
        """
        if self._role is None:
            self._role = BaseDeviceEnum.node
        return self._role
    
    @property
    def address(self):
        """
        If parameters have a `test_address` field uses it
         
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
        Builds a connection to the node
        
        :return: connection built to match parameter.connection
        """
        if self._connection is None:
            self._connection = connection_builders[self.parameters.connection](self.parameters).connection
        return self._connection

    @property
    def interface(self):
        """
        Sets the test interface using parameters.test_interface
        
        :return: the name of the device's test_interface
        :raises: ConfigurationError if test_interface & test_address not given
        """
        if self._interface is None:
            try:
                self._interface = self.parameters.test_interface
            except AttributeError as error:
                self.logger.warning(error)
                message = "Expected in Config-File: section `[{0}]`, option `{1}:<test interface>` (e.g. wlan0)"
                self.logger.warning(message.format(ConfigOptions.nodes_section,
                                                   ConfigOptions.test_interface_option))
                if self.address is None:
                    raise ConfigurationError("Missing the test-interface for {0}".format(self.parameters.connection.hostname))
        return self._interface

    @property
    def node(self):
        """
        The Built Node
        
        :return: device built to match parameter.operating_system
        """
        if self._node is None:
            self._node = device_builders[self.parameters.operating_system](connection=self.connection,
                                                                           interface=self.interface,
                                                                           address=self.address,
                                                                           role=self.role).device
        return self._node
# end class NodeBuilder


class NodeBuilderTypes(object):
    __slots__ = ()
    windows = "windows"
    linux = "linux"
    android = 'android'
    ios = 'ios'
# end class NodeBuilderTypes
