"""
A module to run the NAXXX Network Power Supply 
"""

#python libraries
from types import StringType, IntType
from socket import timeout

# nps libraries
from nps import nps, MAX_PINS

#tottest
from tottest.baseclass import BaseClass
from tottest.commons import errors

AffectorError = errors.AffectorError
ConfigurationError = errors.ConfigurationError

class FaucetteError(ConfigurationError):
    """
    A FaucetteError is raised if a configuration error is detected
    """
    def __init__(self, message=""):
        self.message = message
        return

    def __str__(self):
        message =  """!!!!!!!!!!!!!!!!!    You're blowin' it!     !!!!!!!!!!!!!
        
        {m}

        Allowed PIN IDs: 0 to {x}
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!""".format(m=self.message,
                                                                            x=MAX_PINS)
        return message
    

class NaxxxOn(BaseClass):
    """
    An adapter to the nps to reduce the interface.
    
    """
    def __init__(self, IP, clear=True, retry=5):
        """
        :param:
         - `IP`    : String containing the IP address of the Elexol device.
         - `clear` : Bool indicating whether or not NPS will disable all plugs at start
         - `retry` : Number of times to retry if communication with Elexol fails.
        """ 
        super(NaxxxOn, self).__init__()
        self.naxxx = nps(IP, clear, retry)
        return

    def DisplayError(self, message):
        """
        Overrides the default DisplayError to raise an exception.

        :param:

         - `message`: The error message to send.
         
        :raise: FaucetteError
        """
        self.logger.error(message)
        raise FaucetteError(message)
        return

    def run(self, identifiers):
        """
        Turns on the given identifier's switch.
        Turns off all other switches.

        :param:

         - `identifier`: ID of power switch to turn on. Or list of ID's.

        :raise: AffectorError if socket times-out or there is a problem with the identifiers/
        """
        if type(identifiers) is StringType or type(identifiers) is IntType:
            try:
                identifiers = [int(identifiers)]
            except ValueError as error:
                self.logger.error(error)
                raise FaucetteError("Invalid Identifier(s): {0}".format(identifiers))
        else:
            try:
                identifiers = [int(item) for item in identifiers]
            except TypeError as error:
                self.logger.error(error)
                raise FaucetteError("Unable to turn on {0}".format(identifiers))

            except timeout as error:
                self.logger.error(error)
                raise AffectorError("Connection to the Naxxx timed out - check your LAN connection.")
        self.naxxx.TurnOnList(identifiers, clear=True)
        return
# end class NAXXX
