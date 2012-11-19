from unittest import TestCase
from StringIO import StringIO

from mock import MagicMock

from tottest.watchers.tsharkwatcher import TsharkWatcher, TsharkWatcherEnum

sample = """
Capturing on wlan0
464 packets captured

===================================================================
IO Statistics
Interval: 1.000 secs
Column #0:
                |   Column #0
Time            |frames|  bytes
000.000-001.000     464     68161
===================================================================
"""

line = '000.000-001.000     464     68161'

sample2 = """
Capturing on wlan0
536 packets captured

===================================================================
IO Statistics
Interval: 1.000 secs
Column #0:
                |   Column #0
Time            |frames|  bytes
000.000-001.000     535     78577
001.000-002.000       1       439
===================================================================
"""


class TestTsharkWatcher(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.output = MagicMock()
        self.watcher = TsharkWatcher(output=self.output,
                                     connection=self.connection)
        return

    def test_expression(self):
        match = self.watcher.expression.search(line).groupdict()
        self.assertEqual('464', match[TsharkWatcherEnum.frames])
        self.assertEqual('68161', match[TsharkWatcherEnum.bytes])
        return

    def test_multiline(self):        
        self.connection.tshark.return_value = StringIO(sample2), StringIO("")
        t, frames, byte_count = self.watcher.call_once()
        self.assertEqual(frames,536)
        self.assertEqual(byte_count, 79016)
        return

    def test_stop(self):
        self.assertFalse(self.watcher.stopped)
        self.watcher.stop()
        self.assertTrue(self.watcher.stopped)
# end class TestTsharkWatcher
