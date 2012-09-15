"""
A Networked Radio Switch based on the Naxxx interface.
"""

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

    def __call__(self, addresses=None):
        """
        :param:

         - `addresses`: List of adderesses (node-keys) to turn on.

        :postconditions:

         - `enable_wifi` called on all nodes with address in addresses
         - `disable_wifi` called on all nodes with an address not in addresses
        """
        if addresses is not None:
            for address in addresses:
                self.nodes[address].enable_wifi()

                kill_addresses = [address for address in self.nodes if address not in addresses]
        else:
            kill_addresses = self.nodes.keys()
        for address in kill_addresses:
            self.nodes[address].disable_wifi()
        return
# end class NeRS
