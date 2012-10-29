from unittest import TestCase

from mock import MagicMock

from tottest.watchers.procnetdevwatcher import ProcnetdevWatcher, ProcnetdevWatcherEnum
from tottest.watchers.timestamp import TimestampFormat

sample = """
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    lo:   52989     577    0    0    0     0          0         0    52989     577    0    0    0     0       0          0
 wlan0:   27035     223    0    0    0     0          0         0    34708     301    0    0    0     0       0          0
wlan0-mon: 15683751  116759    0    0    0     0          0         0        0       0    0    0    0     0       0          0
  eth0: 78917734   69440    0    0    0     0          0       334  4920158   33266    0    0    0     0       0          0
"""

line = "wlan0-mon: 15683751  116759    0    0    0     0          0         0        0       0    0    0    0     0       0          0"
interface = 'wlan0-mon'


class TestProcnetdevWatcher(TestCase):
    def setUp(self):
        self.output = MagicMock()
        connection = MagicMock()
        self.watcher = ProcnetdevWatcher(output=self.output, interface=interface,
                                         connection = connection,
                                         interval=1)
        return

    def test_expression(self):
        match = self.watcher.expression.search(line).groupdict()
        self.assertIsNotNone(match)
        self.assertEqual("15683751", match[ProcnetdevWatcherEnum.bytes])
        self.assertEqual("116759", match[ProcnetdevWatcherEnum.packets])
        self.assertEqual('wlan0-mon', match[ProcnetdevWatcherEnum.interface])
        return

    def test_stop(self):
        self.assertFalse(self.watcher.stopped)        
        self.watcher.stop()
        self.assertTrue(self.watcher.stopped)
        return
# end class TestProcnetdevWatcher

class TestTimestampFormat(TestCase):
    def setUp(self):
        self.format = TimestampFormat()
        return

    def test_iperf_format(self):
        return
# end class TestTimestampFormat
