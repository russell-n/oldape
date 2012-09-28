"""
This is a module to hold device builders.

* Each builder expects a single parameter on initialization
* Each builder has a `device` property that will return the built device
"""

from tottest.baseclass import BaseClass
from tottest.devices import adbdevice, windowsdevice, linuxdevice


class WindowsDeviceBuilder(BaseClass):
    """
    A Device Builder for Windows Devices
    """
    def __init__(self, connection, interface=None, address=None):
        """
        :param:

         - `connection`: a connection to the device
        """
        super(WindowsDeviceBuilder, self).__init__()
        self.connection = connection
        self.interface = interface
        self.address = address
        self._device = None
        return

    @property
    def device(self):
        """
        :return: A Windows Device
        """
        if self._device is None:
            self._device = windowsdevice.WindowsDevice(self.connection)
        return self._device
# end class WindowsDeviceBuilder

class LinuxDeviceBuilder(BaseClass):
    """
    A Device Builder for Linux Devices
    """
    def __init__(self, connection, interface=None, address=None):
        """
        :param:

         - `connection`: a connection to the device
         - `interface`: The name of the wireless interface
         - `address`: the test address (if needed)
        """
        super(LinuxDeviceBuilder, self).__init__()
        self.connection = connection
        self.interface = interface
        self.address = address
        self._device = None
        return

    @property
    def device(self):
        """
        :return: A Linux Device
        """
        if self._device is None:
            self._device = linuxdevice.LinuxDevice(self.connection, self.interface, self.address)
        return self._device
# end class LinuxDeviceBuilder

    
class AdbDeviceBuilder(BaseClass):
    """
    A Device Builder builds ADB devices
    """
    def __init__(self, parameters=None):
        """
        :param:

         - `parameters`: Just used to keep the interface uniform
        """
        super(AdbDeviceBuilder, self).__init__()
        self.parameters = parameters
        self._device = None
        return

    @property
    def device(self):
        """
        :return: A device for the dut
        """
        if self._device is None:
            self.logger.debug("building the ADB device for the DUT")
            self._device = adbdevice.AdbDevice()
        return self._device
# end class DutDeviceBuilder

class DeviceBuilderTypes(object):
    __slots__ = ()
    windows = "windows"
    linux = "linux"
# end class DeviceBuilderTypes

device_builders = {DeviceBuilderTypes.windows:WindowsDeviceBuilder,
                   DeviceBuilderTypes.linux:LinuxDeviceBuilder}
