"""
A module to run the NAXXX Network Power Supply 
"""

#python libraries
from types import ListType, TupleType, IntType
from socket import timeout

# nps libraries
from networkedpowersupply import NetworkedPowerSupply
from errors import FaucetteError

#tottest
from tottest.baseclass import BaseClass
from tottest.commons import errors

AffectorError = errors.AffectorError
ConfigurationError = errors.ConfigurationError

class NaxxxError(AffectorError):
    """
    A NaxxxError is raised if there is a problem with the Naxxx
    """
    pass


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
            self.logger.debug("Created {0}".format(self._naxxx))
        return self._naxxx

    def _clean_outlets(self, outlets):
        """
        The option to pass in a single castable object allows the caller
        to pass in a generic parameters object.
        
        :param:

         - `outlets`: List, Tuple, or something castable to an int
         
        :return: list of integers
        """
        if type(outlets) not in (ListType, TupleType):
            try:
                outlets = [int(outlets)]
            except ValueError as error:
                self.logger.error(error)
                raise FaucetteError("Invalid Identifier: {0}".format(outlets))
        else:
            try:
                outlets = [int(outlet) for outlet in outlets]
            except (ValueError, TypeError) as error:
                self.logger.error(error)
                raise FaucetteError("Unable to turn on {0}".format(outlets))
        assert all((type(outlet) is IntType for outlet in outlets))
        return outlets

    def run(self, outlets):
        """
        For each id in outlets, turn on the given outlet
        Turns off all outlets not in outlets.

        :param:

         - `outlets`: ID of power switch to turn on. Or list of ID's.

        :raise:

         - `NaxxxError`: If connection (socket) times-out.
         - `FaucetteError`: If there is a problem with the outlet identifiers.

        :postcondition: Only switches in identifiers are on.
        """
        self.logger.info("Turning on Power Outlet(s): {0}".format(outlets))
        outlets = self._clean_outlets(outlets)
        try:
            self.naxxx.turn_on_switches(outlets, turn_others_off=True)
        except (TypeError, timeout) as error:
            self.logger.error(error)
            raise NaxxxError("Unable to connect to the Naxxx  - check your LAN connection.")
        return
# end class NAXXX
