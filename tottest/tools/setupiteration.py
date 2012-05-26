"""
A module to hold a setup class for a single iteration.
"""

# tottest Libraries
from tottest.baseclass import BaseClass
from sleep import Sleep

class SetupIteration(BaseClass):
    """
    A setupIteration sets-up a test iteration.
    """
    def __init__(self, device, time_to_failure_checker, *args, **kwargs):
        """
        :param:

         - `device`: A device interface.
         - `time_to_failure_checker`: A device that waits until a device has failed.
        """
        super(SetupIteration, self).__init__(*args, **kwargs)
        self.device = device
        self.ttf = time_to_failure_checker
        self._sleep = None
        return

    @property
    def sleep(self):
        if self._sleep is None:
            self._sleep = Sleep()
        return self._sleep

    def run(self, parameters):
        """
        Gets wifi info and displays it on the screen, disables the radio.

        :param:

         - `parameters`: An object with the parameters for ttf and sleep.
        """
        info = self.device.get_wifi_info()
        self.logger.debug(info)
        self.device.wake_screen()
        self.device.display(info)
        self.logger.info("Disabling the Radio")
        self.device.disable_wifi()
        self.logger.info("Waiting for the Device to stop responding")
        self.ttf.run(parameters)

        self.sleep.run(parameters.recovery_time)
        return
# end class SetupIteration
