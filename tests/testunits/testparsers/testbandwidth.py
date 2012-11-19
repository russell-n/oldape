from unittest import TestCase

from tottest.parsers import iperfparser

# human-readable format
LINE = "[  5]  5.0- 6.0 sec   256 KBytes  2.10 Mbits/sec"
LINE2 = "[  4]  7.0- 8.0 sec  0.12 MBytes  0.12 MBytes/sec"
LINE3 = "[  5]  5.0- 6.0 sec  131072 Bytes  1048576 bits/sec"
LINE4 = "[  3]  8.0- 9.0 sec  655360 Bytes  655360 Bytes/sec"
LINE5 = "[ 12]  7.0- 8.0 sec   128 KBytes  1049 Kbits/sec"
LINE6 = "[101]  9.0-10.0 sec  1024 KBytes  1024 KBytes/sec"

#csv
CLINE1 = "20120714055910,192.168.20.91,59210,192.168.20.59,5001,5,8.0-9.0,393216,3145728"

class TestBandwidth(TestCase):
    def setUp(self):
        self.parser = iperfparser.IperfParser(threads=1)
        return

    def check_bandwidth(self, line, expected):
        bandwidth = self.parser(line)
        self.assertAlmostEqual(expected, bandwidth)
        return
    
    def test_mbits(self):
        self.check_bandwidth(LINE, 2.10)
        return

    def test_mbytes(self):
        self.check_bandwidth(LINE2, 0.96)
        return

    def test_bits(self):
        self.check_bandwidth(LINE3, 1.048576)
        return
    
    def test_bytes(self):
        self.check_bandwidth(LINE4, 5.24288)
        return

    def test_kbits(self):
        self.check_bandwidth(LINE5, 1.049)
        return

    def test_kbytes(self):
        self.check_bandwidth(LINE6, 8.192)
        return
    
    def test_csv(self):
        self.check_bandwidth(CLINE1, 3.145728)
