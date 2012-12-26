# Copyright 2012 Russell Nakamura
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
A module to maintain a controller for a networked power-switch
"""

from apetools.baseclass import BaseClass


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
        return "{0}".format(params.identifier)

    def turn_all_off(self):
        """
        :postcondition: all switches turned off       
        """
        for name,switch in self.switches.iteritems():
            self.logger.info("Turning off {1} on {0}".format(switch.host, name))
            switch.all_off()
        return
# end class PowerOn
