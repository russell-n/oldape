"""
A builder of affectors.
"""

from tottest.baseclass import BaseClass
from tottest.affectors.elexol import naxxx

class NaxxxAffectorBuilder(BaseClass):
    """
    An AffectorBuilder builds affectors
    """
    def __init__(self, parameters):
        super(NaxxxAffectorBuilder, self).__init__()
        self.parameters = parameters
        self._affector = None
        return

    @property
    def affector(self):
        """
        :return: A built naxxx or None
        """
        if self._affector is None:
            hostname = self.parameters.hostname
            if hostname is not None:
                self._affector = naxxx.NaxxxOn(IP=hostname)
        return self._affector
# end AffectorBuilder
