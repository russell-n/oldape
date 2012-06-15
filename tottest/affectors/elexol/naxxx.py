"""
A module to run the NAXXX Network Power Supply 
"""

#python libraries
from types import StringType, IntType
from socket import timeout

# nps libraries
from networkedpowersupply import NetworkedPowerSupply
from errors import FaucetteError

#tottest
from tottest.baseclass import BaseClass
from tottest.commons import errors

AffectorError = errors.AffectorError
ConfigurationError = errors.ConfigurationError


class Naxxx(BaseClass):
    """
    An adapter to the nps to reduce the interface.
    
    """
    def __init__(self, hostname, clear=False, retries=5):
        """
        :param:
         - `hostname` : IP address of the Elexol device.
         - `clear` : Bool indicating whether or not NPS will disable all plugs at start
         - `retries` : Number of times to retry if communication with Elexol fails.
        """ 
        super(Naxxx, self).__init__()
        self.hostname = hostname
        self.clear = clear
        self.retries = retries
        self._naxxx = None
        return

    @property
    def naxxx(self):
        """
        :rtype: NetworkedPowerSupply
        :return: Controller for the networked power supply
        """
        if self._naxxx is None:
            self._naxxx = NetworkedPowerSupply(IP=self.hostname,
                                               clear=self.clear,
                                               retry=self.retries)
        return self._naxxx
    
    def run(self, outlets):
        """
        for each id in outlest, turn on the given outlet
        Turns off all outlets not in outlets.

        :param:

         - `outlets`: ID of power switch to turn on. Or list of ID's.

        :raise:

         - `AffectorError`: If socket times-out.
         - `FaucetteError`: If there is a problem with the identifiers.

        :postcondition: Only switches in identifiers are on.
        """
        if type(outlets) in (StringType, IntType):
            try:
                outlets = [int(outlets)]
            except ValueError as error:
                self.logger.error(error)
                raise FaucetteError("Invalid Identifier: {0}".format(outlets))
        else:
            try:
                outlets = [int(outlet) for outlet in outlets]
                self.naxxx.turn_on_list(outlets, turn_others_off=True)
            except TypeError as error:
                self.logger.error(error)
                raise FaucetteError("Unable to turn on {0}".format(outlets))

            except timeout as error:
                self.logger.error(error)
                raise AffectorError("Connection to the Naxxx timed out - check your LAN connection.")
        return
# end class NAXXX
