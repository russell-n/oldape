"""
A module to hold test builders.
"""

from tottest.baseclass import BaseClass
from tottest.tools import iperftest

from iperfcommandbuilder import IperfCommandBuilder 
from tottest.commons import errors
from tottest.commons import enumerations
IperfDirection = enumerations.IperfDirection
ConfigurationError = errors.ConfigurationError

DIRECTION_ERROR = 'Unknown Direction: {0}'
DUT_NAME = 'DUT'
TPC_NAME = 'TPC'

BUILD_SENDER_RECEIVER = "Building the {n} as the {r}."


class IperfTestBuilder(BaseClass):
    """
    A builder of iperf tests
    """
    def __init__(self, config_map):
        """
        :param:

         - `config_map`: a pre-loaded configuration map
        """
        self._test = None
        self._commands = None
        return

    @property
    def commands(self):
        """
        :return: an iperf command builder
        """
        if self._commands is None:
            self._commands = IperfCommandBuilder(config_map=self.config_map)
        return self._commands

    @property
    def test(self):
        """
        :return: an iperf test
        """
        if self._test is None:
            self._test = iperftest.IperfTest(receiver_command=self.commands.server_command,
                                             sender_command=self.commands.client_command)
        return self._test
        
# end class IperfTestBuilder
