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
        self.turn_all_off()
        params = parameters.id_switch.parameters
        self.logger.info("Turning on {0} (switch '{1}')".format(params.identifier, params.switch))
        self.switches[params.identifier](params.switch)
        #self.switches[identifier].close()
        return "id_{0}_switch_{1}".format(params.identifier, params.switch.zfill(2))

    def turn_all_off(self):
        """
        :postcondition: all switches turned off       
        """
        for name,switch in self.switches.iteritems():
            self.logger.info("Turning off {1} on {0}".format(switch, name))
            switch.all_off()
        return
# end class PowerOn
