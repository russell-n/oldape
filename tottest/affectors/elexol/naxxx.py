"""
A module to run the NAXXX Network Power Supply 
"""

#python libraries
import logging
from types import ListType
from socket import timeout

# nps libraries
from nps import nps, MAX_PINS

class AffectorError(Exception):
    pass

class NAXXXOn(nps):
    """
    An extension of the nps to reduce the interface to run()
    """
    def __init__(self, *args, **kwargs):
        super(NAXXXOn, self).__init__(*args, **kwargs)
        logname = "{0}.{1}".format(self.__module__,
                                   self.__class__.__name__)
        self.logger = logging.getLogger(logname)
        return

    def DisplayError(self, msg):
        """
        Overrides the default DisplayError to raise an exception.

        :raise: AffectorError
        """
        message =  """!!!!!!!!!!!!!!!!!    You're blowin' it!     !!!!!!!!!!!!!
        
        {m}
        Possible: 0 to {x}
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!""".format(m=msg,
                                                                            x=MAX_PINS)
        self.logger.error(message)
        raise AffectorError(message)
        return

    def run(self, identifiers):
        """
        Turns on the given identifier's switch.
        Turns off all other switches.

        :param:

         - `identifier`: ID of power switch to turn on. Or list of ID's.

        :raise: AffectorError if socket times-out or there is a problem with the identifiers/
        """
        if not type(identifiers) is ListType:
            identifiers = [int(identifiers)]
        else:
            identifiers = [int(item) for item in identifiers]
        try:
            self.TurnOnList(identifiers, clear=True)
        except TypeError as error:
            self.logger.error("{0}: {1}".format(self.__class__.__name__ ,error))
            raise AffectorError("Unable to turn on {0}".format(" ".join([str(_id) for _id in identifiers])))
        except timeout as error:
            self.logger.error(error)
            raise AffectorError("Connection to the Naxxx timed out - check your LAN connection.")
        return
# end class NAXXX
