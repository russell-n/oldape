from unittest import TestCase

from apetools.parsers import iperfparser

SAMPLE = """
------------------------------------------------------------
Client connecting to kobe, TCP port 5001
TCP window size: 16.0 KByte (default)
------------------------------------------------------------
[  9] local 192.168.10.50 port 43641 connected with 192.168.10.59 port 5001
[  3] local 192.168.10.50 port 43636 connected with 192.168.10.59 port 5001
[  5] local 192.168.10.50 port 43637 connected with 192.168.10.59 port 5001
[  4] local 192.168.10.50 port 43635 connected with 192.168.10.59 port 5001
[  7] local 192.168.10.50 port 43638 connected with 192.168.10.59 port 5001
[  6] local 192.168.10.50 port 43639 connected with 192.168.10.59 port 5001
[  8] local 192.168.10.50 port 43640 connected with 192.168.10.59 port 5001
[ 10] local 192.168.10.50 port 43642 connected with 192.168.10.59 port 5001
[ ID] Interval       Transfer     Bandwidth
[  9]  0.0- 1.0 sec  16.8 MBytes   141 Mbits/sec
[  7]  0.0- 1.0 sec  15.8 MBytes   132 Mbits/sec
[  6]  0.0- 1.0 sec  14.5 MBytes   122 Mbits/sec
[  8]  0.0- 1.0 sec  14.9 MBytes   125 Mbits/sec
[  3]  0.0- 1.0 sec  12.6 MBytes   106 Mbits/sec
[  5]  0.0- 1.0 sec  15.6 MBytes   131 Mbits/sec
[  4]  0.0- 1.0 sec  13.4 MBytes   112 Mbits/sec
[ 10]  0.0- 1.0 sec  10.6 MBytes  89.1 Mbits/sec
[SUM]  0.0- 1.0 sec   114 MBytes   957 Mbits/sec
[  8]  1.0- 2.0 sec  15.0 MBytes   126 Mbits/sec
[  9]  1.0- 2.0 sec  16.0 MBytes   134 Mbits/sec
[  7]  1.0- 2.0 sec  15.6 MBytes   131 Mbits/sec
[  5]  1.0- 2.0 sec  15.2 MBytes   128 Mbits/sec
[  6]  1.0- 2.0 sec  14.6 MBytes   123 Mbits/sec
[ 10]  1.0- 2.0 sec  10.5 MBytes  88.1 Mbits/sec
[  3]  1.0- 2.0 sec  11.5 MBytes  96.5 Mbits/sec
[  4]  1.0- 2.0 sec  14.1 MBytes   118 Mbits/sec
[SUM]  1.0- 2.0 sec   113 MBytes   945 Mbits/sec
[  7]  2.0- 3.0 sec  14.5 MBytes   122 Mbits/sec
[  5]  2.0- 3.0 sec  14.6 MBytes   123 Mbits/sec
[  4]  2.0- 3.0 sec  14.5 MBytes   122 Mbits/sec
[  8]  2.0- 3.0 sec  14.6 MBytes   123 Mbits/sec
[  9]  2.0- 3.0 sec  14.6 MBytes   123 Mbits/sec
[  3]  2.0- 3.0 sec  13.0 MBytes   109 Mbits/sec
[  6]  2.0- 3.0 sec  14.6 MBytes   123 Mbits/sec
[ 10]  2.0- 3.0 sec  12.1 MBytes   102 Mbits/sec
[SUM]  2.0- 3.0 sec   113 MBytes   945 Mbits/sec
[  5]  3.0- 4.0 sec  14.0 MBytes   117 Mbits/sec
[  4]  3.0- 4.0 sec  13.8 MBytes   115 Mbits/sec
[  7]  3.0- 4.0 sec  14.4 MBytes   121 Mbits/sec
[  6]  3.0- 4.0 sec  13.8 MBytes   115 Mbits/sec
[ 10]  3.0- 4.0 sec  13.6 MBytes   114 Mbits/sec
[  9]  3.0- 4.0 sec  15.2 MBytes   128 Mbits/sec
[  8]  3.0- 4.0 sec  13.9 MBytes   116 Mbits/sec
[  3]  3.0- 4.0 sec  13.8 MBytes   115 Mbits/sec
[SUM]  3.0- 4.0 sec   112 MBytes   943 Mbits/sec
[  7]  4.0- 5.0 sec  15.9 MBytes   133 Mbits/sec
[  6]  4.0- 5.0 sec  14.9 MBytes   125 Mbits/sec
[  8]  4.0- 5.0 sec  15.2 MBytes   128 Mbits/sec
[  9]  4.0- 5.0 sec  15.6 MBytes   131 Mbits/sec
[  5]  4.0- 5.0 sec  15.9 MBytes   133 Mbits/sec
[  4]  4.0- 5.0 sec  14.0 MBytes   117 Mbits/sec
[ 10]  4.0- 5.0 sec  10.6 MBytes  89.1 Mbits/sec
[  3]  4.0- 5.0 sec  10.6 MBytes  89.1 Mbits/sec
[SUM]  4.0- 5.0 sec   113 MBytes   946 Mbits/sec
[  5]  5.0- 6.0 sec  15.1 MBytes   127 Mbits/sec
[  6]  5.0- 6.0 sec  15.4 MBytes   129 Mbits/sec
[  3]  5.0- 6.0 sec  14.6 MBytes   123 Mbits/sec
[  4]  5.0- 6.0 sec  15.4 MBytes   129 Mbits/sec
[  8]  5.0- 6.0 sec  12.1 MBytes   102 Mbits/sec
[  9]  5.0- 6.0 sec  15.4 MBytes   129 Mbits/sec
[  7]  5.0- 6.0 sec  11.8 MBytes  98.6 Mbits/sec
[ 10]  5.0- 6.0 sec  12.5 MBytes   105 Mbits/sec
[SUM]  5.0- 6.0 sec   112 MBytes   942 Mbits/sec
[  3]  6.0- 7.0 sec  14.8 MBytes   124 Mbits/sec
[  5]  6.0- 7.0 sec  15.0 MBytes   126 Mbits/sec
[  7]  6.0- 7.0 sec  12.1 MBytes   102 Mbits/sec
[  6]  6.0- 7.0 sec  15.0 MBytes   126 Mbits/sec
[  8]  6.0- 7.0 sec  9.88 MBytes  82.8 Mbits/sec
[  9]  6.0- 7.0 sec  15.4 MBytes   129 Mbits/sec
[  4]  6.0- 7.0 sec  14.9 MBytes   125 Mbits/sec
[ 10]  6.0- 7.0 sec  14.9 MBytes   125 Mbits/sec
[SUM]  6.0- 7.0 sec   112 MBytes   938 Mbits/sec
[  4]  7.0- 8.0 sec  15.4 MBytes   129 Mbits/sec
[  6]  7.0- 8.0 sec  15.9 MBytes   133 Mbits/sec
[  5]  7.0- 8.0 sec  17.1 MBytes   144 Mbits/sec
[  7]  7.0- 8.0 sec  12.8 MBytes   107 Mbits/sec
[  8]  7.0- 8.0 sec  8.50 MBytes  71.3 Mbits/sec
[ 10]  7.0- 8.0 sec  12.6 MBytes   106 Mbits/sec
[  3]  7.0- 8.0 sec  12.9 MBytes   108 Mbits/sec
[  9]  7.0- 8.0 sec  17.9 MBytes   150 Mbits/sec
[SUM]  7.0- 8.0 sec   113 MBytes   948 Mbits/sec
[  5]  8.0- 9.0 sec  18.4 MBytes   154 Mbits/sec
[  6]  8.0- 9.0 sec  18.2 MBytes   153 Mbits/sec
[  8]  8.0- 9.0 sec  8.88 MBytes  74.4 Mbits/sec
[  9]  8.0- 9.0 sec  18.2 MBytes   153 Mbits/sec
[  3]  8.0- 9.0 sec  11.0 MBytes  92.3 Mbits/sec
[  4]  8.0- 9.0 sec  18.1 MBytes   152 Mbits/sec
[ 10]  8.0- 9.0 sec  10.0 MBytes  83.9 Mbits/sec
[  7]  8.0- 9.0 sec  9.88 MBytes  82.8 Mbits/sec
[SUM]  8.0- 9.0 sec   113 MBytes   946 Mbits/sec
[  5]  9.0-10.0 sec  19.8 MBytes   166 Mbits/sec
[  5]  0.0-10.0 sec   161 MBytes   135 Mbits/sec
[  7]  9.0-10.0 sec  7.50 MBytes  62.9 Mbits/sec
[  7]  0.0-10.0 sec   130 MBytes   109 Mbits/sec
[  6]  9.0-10.0 sec  19.8 MBytes   166 Mbits/sec
[  6]  0.0-10.0 sec   157 MBytes   131 Mbits/sec
[  8]  9.0-10.0 sec  7.75 MBytes  65.0 Mbits/sec
[  8]  0.0-10.0 sec   121 MBytes   101 Mbits/sec
[ 10]  9.0-10.0 sec  8.88 MBytes  74.4 Mbits/sec
[ 10]  0.0-10.0 sec   116 MBytes  97.6 Mbits/sec
[  9]  9.0-10.0 sec  20.2 MBytes   170 Mbits/sec
[  9]  0.0-10.0 sec   166 MBytes   139 Mbits/sec
[  4]  9.0-10.0 sec  19.5 MBytes   164 Mbits/sec
[  4]  0.0-10.0 sec   153 MBytes   128 Mbits/sec
[  3]  9.0-10.0 sec  10.1 MBytes  84.9 Mbits/sec
[SUM]  9.0-10.0 sec   114 MBytes   952 Mbits/sec
[  3]  0.0-10.0 sec   125 MBytes   105 Mbits/sec
[SUM]  0.0-10.0 sec  1.10 GBytes   944 Mbits/sec
""".split('\n')

FIRST_SET = """
------------------------------------------------------------
Client connecting to localhost, TCP port 5001
TCP window size: 49.5 KByte (default)
------------------------------------------------------------
[ 10] local 127.0.0.1 port 39245 connected with 127.0.0.1 port 5001
[  3] local 127.0.0.1 port 39239 connected with 127.0.0.1 port 5001
[  5] local 127.0.0.1 port 39238 connected with 127.0.0.1 port 5001
[  6] local 127.0.0.1 port 39240 connected with 127.0.0.1 port 5001
[  4] local 127.0.0.1 port 39241 connected with 127.0.0.1 port 5001
[  9] local 127.0.0.1 port 39242 connected with 127.0.0.1 port 5001
[  8] local 127.0.0.1 port 39243 connected with 127.0.0.1 port 5001
[  7] local 127.0.0.1 port 39244 connected with 127.0.0.1 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 1.0 sec   388 MBytes  3.26 Gbits/sec
[  5]  0.0- 1.0 sec   393 MBytes  3.30 Gbits/sec
[  9]  0.0- 1.0 sec   138 MBytes  1.16 Gbits/sec
[  8]  0.0- 1.0 sec   200 MBytes  1.68 Gbits/sec
[ 10]  0.0- 1.0 sec   140 MBytes  1.17 Gbits/sec
[  6]  0.0- 1.0 sec   187 MBytes  1.57 Gbits/sec
[  4]  0.0- 1.0 sec   219 MBytes  1.84 Gbits/sec
[  7]  0.0- 1.0 sec   136 MBytes  1.14 Gbits/sec
[SUM]  0.0- 1.0 sec  1.76 GBytes  15.1 Gbits/sec
""".split('\n')

THREADS = "3 5 9 8 10 6 4 7".split()
GIGA = 10**3
BANDWIDTHS = "3.26 3.30 1.16 1.68 1.17 1.57 1.84 1.14".split()
BANDWIDTHS = [GIGA * float(b) for b in BANDWIDTHS]


SUMS = "958.1 944.6 947 941 945.2 942.6 939.8 948.3 945.4 953.2".split()
SUMS = [float(s) for s in SUMS]


class TestThreadSums(TestCase):
    def setUp(self):
        self.parser = iperfparser.IperfParser()
        return

    def test_bandwiths(self):
        for line in FIRST_SET:
            self.parser(line)
        self.assertIn(0.0, self.parser.intervals)
        self.assertAlmostEqual(sum(BANDWIDTHS), self.parser.intervals[0.0])
        return

    def test_reset(self):
        for line in FIRST_SET:
            self.parser(line)
        self.parser.reset()
        self.assertIsNone(self.parser.format)
        self.assertIsNone(self.parser._bandwidths)
        return
            
    def test_sums(self):
        self.parser.reset()
        for line in SAMPLE:
            self.parser(line)
        index = 0
        for bandwidth in self.parser.bandwidths:
            self.assertAlmostEqual(SUMS[index], bandwidth)
            index += 1
        return
    
# end class ThreadSums
