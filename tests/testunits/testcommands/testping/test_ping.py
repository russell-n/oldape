"""
A module to test pings
"""

# python
from StringIO import StringIO
from unittest import TestCase

# third party
from mock import MagicMock

from tottest.commons import enumerations
from tottest.commands import ping

class PingCommandTest(TestCase):
    def setUp(self):
        self.target="192.168.20.24"
        self.connection = MagicMock()

    def testandroid(self):
        self.connection.ping.return_value = StringIO(ping_android), None
        pinger = ping.PingCommand(target=self.target,
                                  connection= self.connection,
                                  operating_system = enumerations.OperatingSystem.android)

        result = pinger(connection=self.connection)
        self.assertEqual("98.4", result.rtt)
        self.assertEqual(self.target, result.target)
        return

    def testlinux(self):
        self.connection = MagicMock()
        self.connection.ping.return_value = StringIO(ping_linux), None
        pinger = ping.PingCommand(target=self.target,
                                  connection= self.connection,
                                  operating_system = enumerations.OperatingSystem.linux)
        result = pinger(connection=self.connection)
        self.assertEqual("0.196", result.rtt)
        self.assertEqual(self.target, result.target)
        return
    
ping_android = """
PING 192.168.20.24 (192.168.20.24) 56(84) bytes of data.
64 bytes from 192.168.20.24: icmp_seq=1 ttl=64 time=98.4 ms

--- 192.168.20.24 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 98.450/98.450/98.450/0.000 ms
"""

ping_linux = """
PING 192.168.20.24 (192.168.20.24) 56(84) bytes of data.
64 bytes from 192.168.20.24: icmp_req=1 ttl=64 time=0.196 ms

--- 192.168.20.24 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.196/0.196/0.196/0.000 ms
"""
