"""
A base-device builder to serve as a template
"""

#python standard library
from abc import ABCMeta, abstractproperty

# apetools modules
from apetools.baseclass import BaseClass

class BaseDeviceBuilder(BaseClass):
    """
    A template-class for device-builders
    """
    __metaclass__ = ABCMeta
    def __init__(self, connection, role, interface=None, address=None,
                 csv=False):
        """
        :param:

         - `connection`: a connection to the device
         - `role`: some kind of identifier (e.g. node)
         - `interface`: the name of the test interface
         - `address`: hostname of the test interface
         - `csv`: if true, send output as csv
        """
        super(BaseDeviceBuilder, self).__init__()
        self._logger = None
        self.connection = connection
        self.role = role
        self.interface = interface
        self.address = address
        self.csv = csv
        self._device = None
        return

    @abstractproperty
    def device(self):
        """
        :return: the constructed device
        """
        return self._device
    
# end class BaseDeviceBuilder
