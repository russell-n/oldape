"""
A module to maintain a controller for a networked power-switch
"""

from tottest.baseclass import BaseClass


class PowerOn(BaseClass):
    """
    A class to power-on a networked-switch
    """
    def __init__(self, switches):
        """
        :param:

         - `switches`: A dictionary of identifiers:switches
        """
        super(PowerOn, self).__init__()
        self.switches = switches
        return

    def __call__(self, parameters):
        """
        :param:

         - `parameters`: namedtuple with parameters.id_switch.parameters
        """
        identifier, switch_hostname = parameters.id_switch.parameters
        self.logger.info("Turning on {0} (switch '{1}')".format(identifier, switch_hostname))
        self.switches[identifier](switch_hostname.switch)
        return "id_{0}_switch_{1}".format(identifier, switch_hostname.switch)
# end class PowerOn
