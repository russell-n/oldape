"""
A module to hold test builders.
"""

from tottest.baseclass import BaseClass
from tottest.tools import iperftest
from tottest.tools import killall
from tottest.commands import iperfcommand


class IperfTestToDutBuilder(BaseClass):
    """
    The IperfTestBuilder builds IperfTests
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
        super(IperfTestToDutBuilder, self).__init__()
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
    def sender(self):
        """
        :return: the Iperf client
        """
        if self._sender is None:
            self.logger.debug("Building the TPC as the sender (client).")
            self._sender = iperfcommand.IperfCommand(connection=self.tpc_connection,
                                                     output=self.storage,
                                                     role="tcp_traffic_sent_to_dut")
        return self._sender

    @property
    def receiver(self):
        """
        :return: the Iperf server
        """
        if self._receiver is None:
            self.logger.debug("Building the DUT as receiver (server).")
            self._receiver = iperfcommand.IperfCommand(connection=self.dut_connection,
                                                       output=self.storage,
                                                       role="tcp_traffic_received_by_dut")
        return self._receiver

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
