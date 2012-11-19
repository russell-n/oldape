"""
A Networked Radio Switch based on the Naxxx interface.
"""
from types import StringType

from tottest.baseclass import BaseClass


class NeRS(BaseClass):
    """
    A Networked Radio Switch to enable and disable radios over the network.
    """
    def __init__(self, nodes):
        """
        :param:

         - `nodes`: A dictionary of <address>:Wifi enabler/disabler
        """
        super(NeRS, self).__init__()
        self.nodes = nodes        
        return

    def __call__(self, parameters=None):
        """
        :param:

         - `parameters`: namedtuple with `.ners.parameters` List of addresses (node-keys) to turn on.

        :postconditions:

         - `enable_wifi` called on all nodes with address in addresses
         - `disable_wifi` called on all nodes with an address not in addresses
        """
        if parameters is not None:
            addresses = parameters.nodes.parameters
            if type(addresses) is StringType:
                addresses = [addresses]
            for address in addresses:
                self.logger.info("Enabling: '{0}'".format(address))
                self.nodes[address].enable_wifi()

                kill_addresses = [address for address in self.nodes if address not in addresses]
        else:
            kill_addresses = self.nodes.keys()
        for address in kill_addresses:
            self.logger.info("Disabling: '{0}'".format(address))
            self.nodes[address].disable_wifi()
        return
# end class NeRS
