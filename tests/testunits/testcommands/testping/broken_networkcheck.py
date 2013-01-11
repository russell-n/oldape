from unittest import TestCase
from mock import MagicMock

#from apetools.tools import networkcheck

from apetools.commands import ifconfig, netcfg
from apetools.commands import ping
from apetools.commons import enumerations
from apetools.tools import timetorecovery

# test folder
from ifconfig_samples import ifconfig_linux
from netcfg_samples import netcfg_android

from ping_samples import ping_linux, ping_android, ping_fail_linux, ping_fail_android

NEWLINE = "\n"

class NetworkCheckTest(TestCase):
    def setUp(self):
        self.tpc_pings = [ping_fail_linux, ping_fail_linux, ping_linux]
        self.dut_pings = [ping_fail_android, ping_fail_android, ping_fail_android, ping_android]

    def tpc_ping_effects(self):
        return self.tpc_pings.pop(0)

    def dut_ping_effects(self):
        return self.dut_pings.pop(0)

    def test(self):
        # Setup the mock connections
        dut_connection = MagicMock()
        dut_connection.netcfg.return_value = netcfg_android
        tpc_connection = MagicMock()
        tpc_connection.ifconfig.return_value = ifconfig_linux
        
    # get the ip addresses for the test interfaces
        dut_ip = netcfg.NetcfgCommand(dut_connection, 'wlan0').ip_address
        tpc_ip = ifconfig.IfconfigCommand(tpc_connection, 'eth0').ip_address
        self.assertEqual('192.168.20.51', tpc_ip)
        self.assertEqual("192.168.20.153", dut_ip)

    # get the ping results
        dut_connection.ping.return_value = ping_android
        tpc_connection.ping.return_value = ping_linux
        ping_to_dut = ping.PingCommand(dut_ip, tpc_connection,
                                   enumerations.OperatingSystem.linux)
        ping_to_tpc = ping.PingCommand(tpc_ip, dut_connection,
                                   enumerations.OperatingSystem.android)

        dut_ping = ping_to_dut.run()
        tpc_ping = ping_to_tpc.run()

        self.assertEqual("0.196", dut_ping.rtt)
        self.assertEqual("98.4", tpc_ping.rtt)

    # get the consecutive ping results
        dut_connection.side_effects = self.dut_ping_effects
        tpc_connection.side_effects = self.tpc_ping_effects

        dut_to_pc = timetorecovery.TimeToRecovery(ping_to_tpc, timeout=10, threshold=1)
        pc_to_dut = timetorecovery.TimeToRecovery(ping_to_dut, timeout=10, threshold=1)

        tpc_pinged = dut_to_pc.run()
        dut_pinged = pc_to_dut.run()
    
        self.assertEqual("0.196", dut_pinged.rtt)
        self.assertEqual("98.4", tpc_pinged.rtt)
        return

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    test()
