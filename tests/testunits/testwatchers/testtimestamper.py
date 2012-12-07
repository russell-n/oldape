from unittest import TestCase
import time
from mock import patch, MagicMock

from apetools.watchers.timestamp import TimestampFormat, TimestampFormatEnums

class TestTimestampFormat(TestCase):
    def setUp(self):
        self.format = TimestampFormat()
        return

    def test_iperf_format(self):
        self.format.format_type = TimestampFormatEnums.iperf
        now = 1351460136.807799

        self.assertEqual('20121028143536', time.strftime(self.format.format, time.localtime(now)))
        return

    def test_iperf_now(self):
        self.format.format_type = TimestampFormatEnums.iperf
        strftime = MagicMock()
        strftime.return_value = '20121028143536'
        with patch("time.strftime", strftime):
            self.assertEqual('20121028143536', self.format.now)
        return

    def test_convert(self):
        self.format.format_type = TimestampFormatEnums.iperf
        time = 1351788236.96237
        output = self.format.convert(time)
        self.assertEqual('20121101094356', output)
# end class TestTimestampFormat
