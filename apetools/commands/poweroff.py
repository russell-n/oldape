
from apetools.baseclass import BaseClass


class PowerOff(BaseClass):
    """
    A class to power-off a networked-switch
    """
    def __init__(self, switches):
        """
        :param:

         - `switches`: A dictionary of identifiers:switches
        """
        super(PowerOff, self).__init__()
        self.switches = switches
        return

    def __call__(self, parameters=None, filename_prefix=None):
        """
        :param:

         - `parameters`: namedtuple with parameters.id_switch.parameters
         - `filename_prefix`: Temporary hack until the teardown test is setup
        """
        if parameters is None:
            for key, value in self.switches.iteritems():
                self.logger.info("Turning off: {0}".format(key))
                value()
            return
        identifier, switch_hostname = parameters.id_switch.parameters
        self.logger.info("Turning off switches on {0}".format(switch_hostname))
        self.switches[identifier]()
        # a hack until poweron and off can share the same client
        self.switches[identifier].close()
        return 
# end class PowerOFF
