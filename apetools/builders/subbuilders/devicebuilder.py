"""
This is a module to hold device builders.

* Each builder expects a single parameter on initialization
* Each builder has a `device` property that will return the built device
"""

from basedevicebuilder import BaseDeviceBuilder
from apetools.devices import adbdevice, windowsdevice, linuxdevice, macdevice, hr44device


class WindowsDeviceBuilder(BaseDeviceBuilder):
    """
    A Device Builder for Windows Devices
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: a connection to the device
         - `role`: some kind of identifier (e.g. node)
         - `interface`: the name of the test interface
         - `address`: hostname of the test interface
        """
        super(WindowsDeviceBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def device(self):
        """
        :return: A Windows Device
        """
        if self._device is None:
            self._device = windowsdevice.WindowsDevice(self.connection,
                                                       role=self.role)
        return self._device
# end class WindowsDeviceBuilder

class LinuxDeviceBuilder(BaseDeviceBuilder):
    """
    A Device Builder for Linux Devices
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: a connection to the device
         - `role`: the role (tpc, node)
         - `interface`: The name of the wireless interface
         - `address`: the test address (if needed)
        """
        super(LinuxDeviceBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def device(self):
        """
        :return: A Linux Device
        """
        if self._device is None:
            self._device = linuxdevice.LinuxDevice(connection=self.connection,
                                                   interface=self.interface,
                                                   address=self.address,
                                                   role=self.role)
        return self._device
# end class LinuxDeviceBuilder

    
class AndroidDeviceBuilder(BaseDeviceBuilder):
    """
    A Device Builder builds Android devices
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: a connection to the device
         - `role`: some kind of identifier (e.g. node)
         - `interface`: the name of the test interface
         - `address`: hostname of the test interface
        """
        super(AndroidDeviceBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def device(self):
        """
        :return: A device for the dut
        """
        if self._device is None:
            self.logger.debug("building the ADB device for the DUT")
            self._device = adbdevice.AdbDevice(connection=self.connection,
                                               interface=self.interface,
                                               address=self.address,
                                               role=self.role,
                                               csv=self.csv)
        return self._device
# end class DutDeviceBuilder

class MacDeviceBuilder(BaseDeviceBuilder):
    """
    A Device Builder builds mac os devices
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: a connection to the device
         - `role`: some kind of identifier (e.g. node)
         - `interface`: the name of the test interface
         - `address`: hostname of the test interface
        """
        super(MacDeviceBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def device(self):
        """
        :return: A device for the dut
        """
        if self._device is None:
            self.logger.debug("building the Mac os device for the DUT")
            self._device = macdevice.MacDevice(connection=self.connection,
                                               interface=self.interface,
                                               address=self.address,
                                               role=self.role,
                                               csv=self.csv)
        return self._device
# end class MacDeviceBuilder

class Hr44DeviceBuilder(BaseDeviceBuilder):
    """
    A Device Builder builds mac os devices
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: a connection to the device
         - `role`: some kind of identifier (e.g. node)
         - `interface`: the name of the test interface
         - `address`: hostname of the test interface
        """
        super(Hr44DeviceBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def device(self):
        """
        :return: A device for the dut
        """
        if self._device is None:
            self.logger.debug("building the HR44 device for the DUT")

            self._device = hr44device.HR44Device(connection=self.connection,
                                                 interface=self.interface,
                                                 address=self.address,
                                                 role=self.role,
                                                 csv=self.csv)
        return self._device
# end class MacDeviceBuilder

class DeviceBuilderTypes(object):
    __slots__ = ()
    windows = "windows"
    linux = "linux"
    android = "android"
    mac = 'mac'
    osx = 'mac'
    macintosh = 'mac'
    hr44 = 'hr44'
# end class DeviceBuilderTypes

device_builders = {DeviceBuilderTypes.windows:WindowsDeviceBuilder,
                   DeviceBuilderTypes.linux:LinuxDeviceBuilder,
                   DeviceBuilderTypes.android:AndroidDeviceBuilder,
                   DeviceBuilderTypes.mac:MacDeviceBuilder,
                   DeviceBuilderTypes.hr44:Hr44DeviceBuilder}
