"""
A module to test pings
"""

# python
from StringIO import StringIO

# third party
from mock import MagicMock

from tottest.commons import enumerations
from tottest.commands import ping

from ..common import assert_equal


def testandroid():
    target="192.168.20.24"
    connection = MagicMock()
    connection.ping.return_value = StringIO(ping_android)
    pinger = ping.PingCommand(target=target,
                              connection= connection,
                              operating_system = enumerations.OperatingSystem.android)
    result = pinger.run()
    assert_equal("98.4", result.rtt)
    assert_equal(target, result.target)
    return

def testlinux():
    elin = "192.168.20.24"
    connection = MagicMock()
    connection.ping.return_value = StringIO(ping_linux)
    pinger = ping.PingCommand(target=elin,
                              connection= connection,
                              operating_system = enumerations.OperatingSystem.linux)
    result = pinger.run()
    assert_equal("0.196", result.rtt)
    assert_equal(elin, result.target)
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
