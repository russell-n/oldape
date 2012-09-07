"""
A module to hold a setup class for a single iteration.
"""

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.commons import errors

# Android hack for sucky tates
from tottest.commands import svc
from tottest.commands import dumpsyswifi
from sleep import Sleep

ConfigurationError = errors.ConfigurationError
AffectorError = errors.AffectorError

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
        self._enable_wifi = None
        self._disable_wifi = None
        self._dumpsys = None
        return

    @property
    def dumpsys(self):
        if self._dumpsys is None:
            self._dumpsys = dumpsyswifi.DumpsysWifi()
        return self._dumpsys
        
    @property
    def enable_wifi(self):
        """
        An Android radio enabler to try and keep the Tate's alive
        """
        if self._enable_wifi is None:
            self._enable_wifi = svc.EnableWifi(connection=self.device)
        return self._enable_wifi

    @property
    def disable_wifi(self):
        """
        Android radio disabler
        """
        if self._disable_wifi is None:
            self._disable_wifi = svc.DisableWifi(connection=self.device)
        return self._disable_wifi
    
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
        self.logger.warning("Tate-based hacks coming up")
        self.log("Disabling the radio")
        self.disable_wifi()
        self.sleep.run(5)
        self.log("Enabling the radio")
        self.enable_wifi()
        self.sleep.run(5)
        self.affector.run(parameters.affector)
        recovery_time = self.time_to_recovery.run()
        if not recovery_time:
            try:
                o,e = self.device.wl("rssi")
                self.log("rssi: {0} -dbm".format("".join([line.rstrip() for line in o])))
            except Exception as error:
                self.logger.error(error)
            raise AffectorError("Unable to recover from environmental affect")

        self.log("Time to recovery: {0}".format(recovery_time))

        self.sleep.run(5)
        self.logger.warning("Another tate hack")
        self.log("Signal Strength: {0}".format(self.dumpsys.rssi))
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
