"""
A configurer and queryier for the messed up hr44
"""

from apetools.commands.ifconfig import IfconfigCommand
from apetools.commands.iwconfig import Iwconfig
from apetools.commons.enumerations import OperatingSystem
from apetools.devices.linuxdevice import LinuxDevice

class HR44Device(LinuxDevice):
    """
    A class to configure and query hr44 devices
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: a connection to the device
         - `interface`: the name of the test interface (to get the ip address)
        """
        super(HR44Device, self).__init__(*args, **kwargs)
        self._ifconfig = None
        self._wifi_query = None
        return

    @property
    def ifconfig(self):
        """
        :return: ifconfig command
        """
        if self._ifconfig is None:
            self._ifconfig = IfconfigCommand(connection=self.connection,
                                             interface = self.interface,
                                             path='/sbin',
                                             operating_system=OperatingSystem.linux)
        return self._ifconfig

    @property
    def wifi_query(self):
        """
        :return: wifi_query command
        """
        if self._wifi_query is None:
            self._wifi_query = Iwconfig(connection=self.connection,
                                      interface=self.interface,
                                      path='/opt/wlanmanager/thirdparty/bin/')
        return self._wifi_query
# end class LinuxDevice
