"""
A set of tests that check different cases for the ttr
"""
#python
from types import NoneType
from unittest import TestCase
#third-party
from mock import MagicMock

#from tottest.tools import networkcheck

from tottest.commands import ping
from tottest.commons import enumerations
from tottest.tools import timetorecovery

# test folder

#from ..common import assert_equal, assert_is
from ping_samples import ping_linux, ping_linux_2, ping_linux_3
from ping_samples import ping_linux_rtt, ping_linux_3_rtt
from ping_samples import ping_fail_linux

dut_ip = "192.168.20.153"

class TimeToRecoverTest(TestCase):
    
    def test_case_1(self):
        """
        :description: first of 5 pings is returned after failed pings

        :assert: the returned rtt matches the first ping's rtt
        """
    # setup the simulated pings
        tpc_pings = [ping_fail_linux, ping_fail_linux, ping_linux] + [ping_linux_2] * 4

        def side_effects(*args, **kwargs):
            return tpc_pings.pop(0)

    # Setup the mock connection to the tpc (linux)
        tpc_connection = MagicMock()
        ping_to_dut = ping.PingCommand(dut_ip, tpc_connection,
                                       enumerations.OperatingSystem.linux)
       
    # get the consecutive ping results

        tpc_connection.ping.side_effect = side_effects

    #ping_to_dut = MagicMock(side_effects=tpc_pings)
        pc_to_dut = timetorecovery.TimeToRecovery(ping_to_dut, timeout=10, threshold=5)

        dut_pinged = pc_to_dut.run()

        self.assertEqual(ping_linux_rtt, dut_pinged.rtt)
        return

    def test_case_2(self):
        """
        :description: Never successfully pings
        
        :assert: return is None
        """
    # setup the mock
        tpc_connection = MagicMock()

    # setup the ping command
        ping_to_dut = ping.PingCommand(dut_ip, tpc_connection,
                                       enumerations.OperatingSystem.linux)
    # always return a fail when pinging
        tpc_connection.ping.return_value = ping_fail_linux
    # Note: this will take 5 seconds to timeout so it slows down the testing
        pc_to_dut = timetorecovery.TimeToRecovery(ping_to_dut, timeout=5, threshold=5)
        dut_pinged = pc_to_dut.run()
        self.assertEqual(NoneType, type(dut_pinged))
        return

    def test_case_3(self):
        """
        :description: pings, fails, pings to threshold
        """
    # setup the simulated pings
        tpc_pings = ([ping_fail_linux, ping_fail_linux, ping_linux] + [ping_linux_2] * 2 +
                     [ping_fail_linux] + [ping_linux_3] * 5)
        def side_effects(*args, **kwargs):
            return tpc_pings.pop(0)
        
    # setup the connection simulator
        tpc_connection = MagicMock()
        tpc_connection.ping.side_effect = side_effects
        
        ping_to_dut = ping.PingCommand(dut_ip, tpc_connection,
                                       enumerations.OperatingSystem.linux)
        pc_to_dut = timetorecovery.TimeToRecovery(ping_to_dut, timeout=5, threshold=5)
        dut_pinged = pc_to_dut.run()
        self.assertEqual(ping_linux_3_rtt, dut_pinged.rtt)
        return

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    test_case_1()
