"""
A module to hold test builders.
"""

from tottest.baseclass import BaseClass
from tottest.tools import iperftest
from tottest.tools import killall
from tottest.commands import iperfcommand
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
    IperfTestBuilder is a base for IperfTestToDutBuilder and IperfTestFromDutBuilder
    """
    def __init__(self, tpc_connection, dut_connection, storage,
                 command="iperf"):
        """
        :param:

         - `tpc_connection`: A connection to the traffic-pc to build the Iperf Commands
         - `dut_connection`: A connection to the DUT to build the iperf commands
         - `storage`: A storage object to save the output of the iperf commands.
         - `command`: The name of the process to look for when killing       
        """
        super(IperfTestBuilder, self).__init__()
        self.tpc_connection = tpc_connection
        self.dut_connection = dut_connection
        self.storage = storage
        self.command = command
        
        self._sender = None
        self._receiver = None
        self._killers = None
        self._test = None
        return



    @property
    def killers(self):
        """
        :return: tuple of iperf killers
        """
        if self._killers is None:
            self.logger.debug("building a killer for {n} from {c}".format(n=self.command,
                                                                          c=self.tpc_connection))
            tpc = killall.KillAll(connection=self.tpc_connection,
                                  name=self.command)

            self.logger.debug("Building a killer for {n} from {c}".format(n=self.command,
                                                                          c=self.dut_connection))
            dut = killall.KillAll(connection=self.dut_connection,
                                  name=self.command)
            self._killers = ((tpc, dut))
        return self._killers

    @property
    def test(self):
        """
        :return: An iperf test object that runs traffic to the dut.
        """
        if self._test is None:
            self.logger.debug("Building the iperf test (TCP -> DUT)")
            self._test = iperftest.IperfTest(sender=self.sender,
                                                  receiver=self.receiver,
                                                  killers=self.killers)                                                  
        return self._test
# end class IperfTestBuilder

class IperfTestToDutBuilder(IperfTestBuilder):
    """
    The IperfTestToDutBuilder builds tests to the dut
    """
    def __init__(self, *args, **kwargs):
        super(IperfTestToDutBuilder, self).__init__(*args, **kwargs)
        self._logger = None

    @property
    def sender(self):
        """
        :return: the Iperf client
        """
        if self._sender is None:
            role="sender"
            name = TPC_NAME
            self.logger.debug(BUILD_SENDER_RECEIVER.format(n=name, r=role))
            self._sender = iperfcommand.IperfCommand(connection=self.tpc_connection,
                                                     output=self.storage,
                                                     role="traffic_sent_to_dut",
                                                     name=name)
        return self._sender

    @property
    def receiver(self):
        """
        :return: the Iperf server
        """
        if self._receiver is None:
            role = 'receiver'
            self.logger.debug(BUILD_SENDER_RECEIVER.format(n=DUT_NAME, r=role))
            self._receiver = iperfcommand.IperfCommand(connection=self.dut_connection,
                                                       output=self.storage,
                                                       
                                                       role="traffic_received_by_dut",
                                                       name=DUT_NAME)
        return self._receiver

# end class IperfTestBuilder

class IperfTestFromDutBuilder(IperfTestBuilder):
    """
    The IperfTestFromDutBuilder builds tests running traffic from the dut
    """
    @property
    def sender(self):
        """
        :return: the Iperf client
        """
        if self._sender is None:
            role="sender"
            self.logger.debug(BUILD_SENDER_RECEIVER.format(n=DUT_NAME, r=role))
            self._sender = iperfcommand.IperfCommand(connection=self.dut_connection,
                                                     output=self.storage,
                                                     role='traffic_sent_to_tpc',
                                                     name=DUT_NAME)
        return self._sender

    @property
    def receiver(self):
        """
        :return: the Iperf server
        """
        if self._receiver is None:
            role = 'receiver'
            self.logger.debug(BUILD_SENDER_RECEIVER.format(n=TPC_NAME, r=role))
            self._receiver = iperfcommand.IperfCommand(connection=self.tpc_connection,
                                                       output=self.storage,
                                                       role="traffic_received_by_tpc",
                                                       name=TPC_NAME)
        return self._receiver

# end class IperfTestFromDutBuilder
