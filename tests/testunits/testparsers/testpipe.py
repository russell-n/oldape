from unittest import TestCase
from mock import MagicMock

from tottest.parsers.iperfparser import IperfParser
from tottest.parsers.sumparser import SumParser

FRAGMENT = """
------------------------------------------------------------
Client connecting to 192.168.20.99, TCP port 5001
TCP window size: 16.0 KByte (default)
------------------------------------------------------------
[  6] local 192.168.20.50 port 57069 connected with 192.168.20.99 port 5001
[  4] local 192.168.20.50 port 57066 connected with 192.168.20.99 port 5001
[  5] local 192.168.20.50 port 57067 connected with 192.168.20.99 port 5001
[  3] local 192.168.20.50 port 57068 connected with 192.168.20.99 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 1.0 sec   896 KBytes  7.34 Mbits/sec
[  6]  0.0- 1.0 sec   768 KBytes  6.29 Mbits/sec
[  4]  0.0- 1.0 sec   768 KBytes  6.29 Mbits/sec
[  5]  0.0- 1.0 sec   768 KBytes  6.29 Mbits/sec
[SUM]  0.0- 1.0 sec  3.12 MBytes  26.2 Mbits/sec
[  3]  1.0- 2.0 sec   768 KBytes  6.29 Mbits/sec
[  4]  1.0- 2.0 sec   768 KBytes  6.29 Mbits/sec
""".split("\n")

CSV_FRAGMENT = """
20120912102944,192.168.20.50,56843,192.168.20.99,5001,4,0.0-1.0,786432,6291456
20120912102945,192.168.20.50,56844,192.168.20.99,5001,6,0.0-1.0,655360,5242880
20120912102945,192.168.20.50,56842,192.168.20.99,5001,5,0.0-1.0,655360,5242880
20120912102945,192.168.20.50,56841,192.168.20.99,5001,3,0.0-1.0,655360,5242880
20120912102945,192.168.20.50,0,192.168.20.99,5001,-1,0.0-1.0,2752512,22020096
20120912102946,192.168.20.50,56841,192.168.20.99,5001,3,1.0-2.0,655360,5242880
20120912102946,192.168.20.50,56844,192.168.20.99,5001,6,1.0-2.0,917504,7340032
""".split("\n")

class TestPipe(TestCase):
    def setUp(self):
        self.parser = IperfParser()
        return

    def test_human_pipe(self):
        target = MagicMock()
        pipe = self.parser.pipe(target)
        for line in FRAGMENT:
            pipe.send(line)
        expected = 26.21
        name, args, kwargs =  target.send.mock_calls[0]
        actual =  float(args[0])
        self.assertAlmostEqual(expected, actual)
        return

    def test_csv(self):
        target = MagicMock()
        pipe = self.parser.pipe(target)
        for line in CSV_FRAGMENT:
            pipe.send(line)
        expected = 22.020096
        name, args, kwargs = target.send.mock_calls[0]
        actual = float(args[0])
        self.assertAlmostEqual(expected, actual)
        return
# end class TestPipe
        
class TestSumParser(TestCase):
    def setUp(self):
        self.target = MagicMock()
        self.parser = SumParser()
        self.pipe = self.parser.pipe(self.target)
        return

    def test_human_pipe(self):
        self.parser.reset()
        target = MagicMock()
        pipe = self.parser.pipe(target)
        for line in FRAGMENT:
            pipe.send(line)
        expected = 26.2
        print target.send.mock_calls
        name, args, kwargs =  target.send.mock_calls[0]
        actual =  float(args[0])
        self.assertAlmostEqual(expected, actual)
        return

    def test_csv(self):
        for line in CSV_FRAGMENT:
            self.pipe.send(line)
        expected = 22.020096
        name, args, kwargs =  self.target.send.mock_calls[0]
        actual =  float(args[0])
        self.assertAlmostEqual(expected, actual)
        return
# end class TestSumParser

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    parser = IperfParser()
    target = MagicMock()
    pipe = parser.pipe(target)
    for line in FRAGMENT:
        pipe.send(line)
    expected = 26.2
    print target.send.mock_calls
    name, args, kwargs =  target.send.mock_calls[0]
    actual =  float(args[0])
    
