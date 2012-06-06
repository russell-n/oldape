"""
This is a module to hold a device builder
"""

from tottest.baseclass import BaseClass
from tottest.devices import adbdevice

class DutDeviceBuilder(BaseClass):
    """
    A Device Builder builds DUT devices
    """
    def __init__(self, parameters=None):
        """
        :param:

         - `parameters`: Depending on the device being built, this might have values for the device
        """
        super(DutDeviceBuilder, self).__init__()
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
