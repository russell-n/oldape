"""
A module to hold a setup class for a single iteration.
"""

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.commons import errors
from sleep import Sleep

ConfigurationError = errors.ConfigurationError


class SetupIteration(BaseClass):
    """
    A setupIteration sets-up a test iteration.
    """
    def __init__(self, device, affector, time_to_recovery, *args, **kwargs):
        """
        :param:

         - `device`: Connection to the device to send log information to.
         - `affector`: An environmental affector
         - `time_to_recovery`: A device that waits until a device has recovered.
        """
        super(SetupIteration, self).__init__(*args, **kwargs)
        self.device = device
        self.affector = affector
        self.time_to_recovery = time_to_recovery
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
        self.affector.run(parameters.affector)
        recovery_time = self.time_to_recovery.run()
        if not recovery_time:
            raise ConfigurationError("Unable to recover from environmental affect")

        self.log("Time to recovery: {0}".format(recovery_time))
        self.sleep.run(parameters.recovery_time)
        return

    def log(self, message):
        """
        :param:

         - `message`: A String to send to the loggers

        :postcondition: message sent to device log and self.logger
        """
        self.device.log(message)
        self.logger.info(message)
        return
# end class SetupIteration
