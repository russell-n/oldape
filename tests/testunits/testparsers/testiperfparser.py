from unittest import TestCase

from tottest.parsers import iperfparser
ParserKeys = iperfparser.ParserKeys

# human-readable format
LINE = "[  5]  5.0- 6.0 sec   256 KBytes  2.10 Mbits/sec"
LINE2 = "[  4]  7.0- 8.0 sec  0.12 MBytes  0.12 MBytes/sec"
LINE3 = "[  5]  5.0- 6.0 sec  131072 Bytes  1048576 bits/sec"
LINE4 = "[  3]  8.0- 9.0 sec  655360 Bytes  655360 Bytes/sec"
LINE5 = "[ 12]  7.0- 8.0 sec   128 KBytes  1049 Kbits/sec"
LINE6 = "[101]  9.0-10.0 sec  1024 KBytes  1024 KBytes/sec"

LINES = [LINE, LINE2, LINE3, LINE4, LINE5, LINE6]

THREADS = "5 4 5 3 12 101".split()
STARTS = "5.0 7.0 5.0 8.0 7.0 9.0".split()
ENDS = "6.0 8.0 6.0 9.0 8.0 10.0".split()
TRANSFERS = "256 0.12 131072 655360 128 1024".split()
BANDWIDTHS = "2.10 0.12 1048576 655360 1049 1024".split()
UNITS = "Mbits MBytes bits Bytes Kbits KBytes".split()

#csv-format
CLINE1 = "20120714055910,192.168.20.91,59210,192.168.20.59,5001,5,8.0-9.0,393216,3145728"
CLINE2 = "20120716144013,192.168.10.51,0,192.168.10.59,5001,-1,2.0-3.0,111542272,892338176"

TIMESTAMPS = "20120714055910".split()
CTRANSFERS = "393216".split()
CSTARTS = "8.0".split()
CENDS = "9.0".split()
CBANDWIDTHS = "3145728".split()
CSENDER_IPS = "192.168.20.91".split()
CSENDER_PORTS = "59210".split()
CRECEIVER_IPS = "192.168.20.59".split()
CRECEIVER_PORTS = "5001".split()
CTHREADS = "5"

class TestIperfParser(TestCase):
    def setUp(self):
        self.parser = iperfparser.IperfParser()
        self.matches = [self.parser.regex[ParserKeys.human].search(line).groupdict() for line in LINES]
        self.transfers = TRANSFERS
        self.starts = STARTS
        self.ends = ENDS
        self.bandwidths = BANDWIDTHS
        self.threads = THREADS
        return

    def assert_equal(self, key, expected):
        for index, match in enumerate(self.matches):
            self.assertEqual(match[key], expected[index])
        return
    
    def test_thread(self):
        self.assert_equal(ParserKeys.thread, self.threads)
        return

    def test_start(self):
        self.assert_equal(ParserKeys.start, self.starts)
        return

    def test_end(self):
        self.assert_equal(ParserKeys.end, self.ends)
        return

    def test_transfer(self):
        self.assert_equal(ParserKeys.transfer, self.transfers)
        return
    
    def test_bandwith(self):
        self.assert_equal(ParserKeys.bandwidth, self.bandwidths)
        return

    def test_units(self):
        self.assert_equal(ParserKeys.units, UNITS)
        return
# end class TestIperfParser

class TestIperfParserCSV(TestIperfParser):
    """
    Tests the '-y C' output
    """
    def setUp(self):
        self.parser = iperfparser.IperfParser()
        self.match1 = self.parser.regex[ParserKeys.csv].search(CLINE1).groupdict()
        self.matches = [self.match1]
        self.transfers = CTRANSFERS
        self.starts = CSTARTS
        self.ends = CENDS
        self.bandwidths = CBANDWIDTHS
        self.sender_ips = CSENDER_IPS
        self.sender_ports = CSENDER_PORTS
        self.receiver_ips = CRECEIVER_IPS
        self.receiver_ports = CRECEIVER_PORTS
        self.threads = CTHREADS
        return

    def test_timestamp(self):
        self.assert_equal(ParserKeys.timestamp, TIMESTAMPS)
        return

    def test_units(self):
        return

    def test_sender_ip(self):
        self.assert_equal(ParserKeys.sender_ip, self.sender_ips)
        return

    def test_sender_port(self):
        self.assert_equal(ParserKeys.sender_port, self.sender_ports)
        return

    def test_receiver_ip(self):
        self.assert_equal(ParserKeys.receiver_ip, self.receiver_ips)
        return

    def test_receiver_port(self):
        self.assert_equal(ParserKeys.receiver_port, self.receiver_ports)
        return

    def test_sum_line(self):
        self.assertNotRegexpMatches(CLINE2, self.parser.regex[ParserKeys.csv].pattern)
# end TestIperfParserCSV


HLINE = "[  3]  8.0- 9.0 sec  35.4 MBytes   297 Mbits/sec"

class TestIperfParserSearch(TestCase):
    def setUp(self):
        self.parser = iperfparser.IperfParser(threads=1)
        return

    def test_human(self):
        parser = iperfparser.IperfParser(threads=1)
        match = parser(HLINE)
        self.assertEqual(ParserKeys.human, parser.format)
        self.assertAlmostEqual(match, 297)
        return

    def test_csv(self):
        match = self.parser(CLINE1)
        self.assertEqual(ParserKeys.csv, self.parser.format)
        self.assertAlmostEqual(match, 3.145728)
        return


    def test_non_data(self):
        match = self.parser(CLINE2)
        self.assertIsNone(self.parser.format)
        self.assertIsNone(match)
        return
# end class TestIperfParserSearch

INVHLINE = "[  5]  0.0-10.0 sec   321 MBytes   269 Mbits/sec"
INVCLINE = "20120717125325,192.168.10.51,55391,192.168.10.59,5001,3,0.0-10.0,440401920,352095737"

class TestIperfParserValidate(TestCase):
    def setUp(self):
        self.parser = iperfparser.IperfParser(threads=1)
        return

    def test_human_valid(self):
        parser = iperfparser.IperfParser(threads=1)
        bandwidth = parser(HLINE)
        self.assertEqual(297, bandwidth)
        return

    def test_human_invalid(self):
        parser = iperfparser.IperfParser(threads=1)
        bandwidth = parser(INVHLINE)
        self.assertIsNone(bandwidth)
        return

    def test_csv_valid(self):        
        match = self.parser(CLINE1)
        self.assertAlmostEqual(3.145728,match)

    def test_csv_invalid(self):
        match = self.parser(INVCLINE)
        self.assertIsNone(match)
# end class TestIperfParserValidate

if __name__ == "__main__":
    import pudb
    pudb.set_trace()
    parser = iperfparser.IperfParser(threads=1)
    match = parser(HLINE)
    parser.valid(match)
