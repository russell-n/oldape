"""
This is a module to hold device builders.

* Each builder expects a single parameter on initialization
* Each builder has a `device` property that will return the built device
"""

from tottest.baseclass import BaseClass
from tottest.devices import adbdevice

class AdbDeviceBuilder(BaseClass):
    """
    A Device Builder builds DUT devices
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
