from unittest import TestCase
from collections import namedtuple
from StringIO import StringIO

from mock import MagicMock
from nose.tools import raises

from tottest.tools.timetorecovery import TimeToRecovery
from tottest.commons.enumerations import OperatingSystem
from tottest.commons.errors import CommandError

Parameters = namedtuple("Parameters", "nodes target".split())
ParametersNodes = namedtuple("ParametersNodes", "parameters".split())
ParametersTarget = namedtuple("ParametersTarget", "parameters".split())


WINDOWS_OUTPUT = """

Pinging 192.168.10.1 with 32 bytes of data:
Reply from 192.168.10.1: bytes=32 time=1ms TTL=255

Ping statistics for 192.168.10.1:
    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 1ms, Maximum = 1ms, Average = 1ms
"""


WINDOWS_FAILURE = """

Pinging 192.168.10.198 with 32 bytes of data:
Request timed out.

Ping statistics for 192.168.10.198:
    Packets: Sent = 1, Received = 0, Lost = 1 (100% loss),
"""


class TestTimeToRecovery(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.device = MagicMock()
        self.device.connection = self.connection
        nodes = {"a":self.device}
        self.tool = TimeToRecovery(nodes=nodes)
        return

    def test_call_windows(self):
        self.connection.operating_system = OperatingSystem.windows
        self.connection.ping.return_value = StringIO(WINDOWS_OUTPUT), ""
        pn = ParametersNodes("a")
        pt = ParametersNodes("igor")
        p = Parameters(pn, pt)
        self.tool.threshold = 1
        ttr = self.tool(p)
        
        self.connection.ping.assert_called_with("-n 1 -w 1000 igor", timeout=1)
        self.assertIsNotNone(ttr)
        return

    @raises(CommandError)
    def test_failue(self):
        self.connection.operating_system = OperatingSystem.windows
        self.connection.ping.return_value = StringIO(WINDOWS_FAILURE), ""
        pn = ParametersNodes("a")
        pt = ParametersNodes("igor")
        p = Parameters(pn, pt)
        self.tool.timeout = 1        
        self.tool.threshold = 1
        self.tool(p)
        return
# end class TestTimeToRecovery


if __name__ == "__main__":
    import pudb; pudb.set_trace()
    connection = MagicMock()
    connection.operating_system = OperatingSystem.windows
    connection.ping.return_value = StringIO(WINDOWS_FAILURE), ""
    pn = ParametersNodes("a")
    pt = ParametersTarget("igor")
    p = Parameters(pn, pt)
    device = MagicMock()
    device.connection = connection
    nodes = {"a":device}
    tool = TimeToRecovery(nodes=nodes)
    tool.threshold = 1
    tool.timeout = 2
    tool(p)
    connection.assert_called_with("-n 1 -w 1000 igor")
