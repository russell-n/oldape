from unittest import TestCase
import time
from mock import patch, MagicMock

from tottest.watchers.timestamp import TimestampFormat, TimestampFormatEnum

class TestTimestampFormat(TestCase):
    def setUp(self):
        self.format = TimestampFormat()
        return

    def test_iperf_format(self):
        self.format_type.format = TimestampFormatEnum.iperf
        strftime = MagicMock()
        now = 1351460136.807799

        self.assertEqual('201210143536', time.strftime(self.format.format, time.localtime(now)))
        return
# end class TestTimestampFormat
