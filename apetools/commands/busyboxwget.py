
#python Libraries
import re
import time
from collections import namedtuple
# apetools Libraries
from apetools.baseclass import BaseClass
from apetools.parsers import oatbran


EMPTY_STRING = ''
NA = 'NA'
UNKNOWN_HOST = 'unknown host'
NEWLINE = "\n"
# server was there, but now it stopped responding:
SERVER_DOWN = 'no response from server'
# There's a server there but your path might be bad
BAD_URL = 'HTTP/1.1 404 Not Found'
# the server isn't reachable
BAD_ADDRESS = "No route to host"
# server is there but it probably doesn't allow access
NO_RESPONSE = "Connection timed out"
# not a web-server
NOT_A_SERVER= "Connection refused"
ERRORS = [SERVER_DOWN, BAD_URL,
          BAD_ADDRESS, NO_RESPONSE, NOT_A_SERVER]


attributes = 'elapsed error percentage kbits'

HEADER = 'Elapsed(seconds),Complete(%),Size,Error\n'

class BusyboxWgetData(namedtuple('BusyboxWgetData', attributes)):
    """
    A named-tuple to hold the data returned by the `run` call
    """
    __slots__ = ()

    def __str__(self):
        return "{elapsed},{complete},{kbits},{error}".format(elapsed=self.elapsed,
                                                             complete=self.percentage,
                                                             kbits=self.kbits,
                                                             error=self.error)
        


class BusyboxEnum(object):
    """
    A holder of constants
    """
    __slots__ = ()
    destination = 'destination'
    percentage_completed = 'percentage'
    kbits_transferred = 'kbits_transferred'
# end BusyboxEnum        


class BusyboxWget(BaseClass):
    """
    Does a wget and times it.
    """
    def __init__(self, url, connection, timeout=2, destination='/dev/null'):
        """
        BusyboxWget Constructor
        
        :param:

         - `url`: A URL to pull from
         - `connection`: A Connection to the device
         - `timeout`: amount of time to wait before timing out
         - `destination`: place to send the output (expects alpha-num+underscore with / for sub-folders)
        """
        super(BusyboxWget, self).__init__()
        self.url = url
        self.connection = connection
        self.timeout = timeout
        self.destination = destination
        self._arguments = None
        self._expression = None
        return

    @property
    def expression(self):
        """
        A compiled regular expression to match the output.
        """
        if self._expression is None:
            # wget seems to only show the file name, not the full path
            destination = oatbran.NAMED(n=BusyboxEnum.destination,
                                        e=oatbran.ALPHA_NUMS)
            # since the name of the group says percentage, the % is not included
            percentage = oatbran.NAMED(n=BusyboxEnum.percentage_completed,
                                       e=oatbran.INTEGER) + '%' 
            expression = destination + oatbran.SPACES + percentage + oatbran.SPACES
            expression += '\|' + oatbran.CLASS('*\s') + oatbran.ZERO_OR_MORE + '\|'
            # busybox seems to change between k and M so units are included
            expression += oatbran.SPACES + oatbran.NAMED(n=BusyboxEnum.kbits_transferred,
                                                         e=oatbran.INTEGER + '[kM]')
            expression += oatbran.SPACES

            # elapsed time
            expression += ":".join([oatbran.DIGIT * 2]*3) + oatbran.SPACES + 'ETA'

            # sometimes multiple data lines are concanetnated so we want the last one
            # but sometimes error strings are also concatenated so match that too
            expression += oatbran.GROUP(oatbran.STRING_END + oatbran.OR + 'wget:')
            
            self._expression = re.compile(expression)
        return self._expression
        

    @property
    def arguments(self):
        """
        :return: The busybox arguments to use
        """
        if self._arguments is None:
            self._arguments = "wget {url} -O {output} -T {timeout}".format(url=self.url,
                                                                           output=self.destination,
                                                                           timeout=self.timeout)
        return self._arguments
    
    def run(self):
        """
        Executes a single wget

        :return: WgetData or None
        """
        start, data_match, error_string = time.time(), None, EMPTY_STRING
        output, error = self.connection.busybox(self.arguments, timeout=1)

        for line in output:
            line = line.strip()
            if len(line):
                self.logger.debug(line)
                match = self.expression.search(line)
                if match is not None:
                    data_match = match

                if 'wget:' in line: # this seems to only show up on error
                    error_string = line.split(':')[-1].strip()
                    self.logger.error(error_string)
        elapsed = time.time() - start
        self.logger.info("Wget Elapsed Time: {0} seconds".format(elapsed))
        # if it's a busybox error it wil be in stdout, not stderr
        err = error.readline()
        if len(err):
            self.logger.error(err)
        if data_match is not None:
            return BusyboxWgetData(elapsed=elapsed,
                                   percentage=data_match.group(BusyboxEnum.percentage_completed),
                                   kbits=data_match.group(BusyboxEnum.kbits_transferred),
                                   error=error_string)
        return BusyboxWgetData(elapsed=elapsed,
                               percentage=NA,
                               kbits=NA,
                               error=error_string)

    def __call__(self, parameters=None):
        """
        Executes a single wget, checks for a success, returns data

        :param:

         - `parameters`: Not used -- set things up in the constructor (or assign values)
        
        :return: WgetData or None
        :raise: ConfigurationError if the target is unknown
        """
        return self.run()
# end class BusyboxWget


# python standard library
import unittest
import random
import string
from StringIO import StringIO

# third-party
from mock import MagicMock, patch


SAMPLE='''
Connecting to 192.168.20.50:8000 (192.168.20.50:8000)

null                 100% |*******************************| 65536k 00:00:00 ETA




'''.split(NEWLINE)
COMPLETED_LINE = 'null                 100% |*******************************| 65536k 00:00:00 ETA'
DESTINATION = 'null'
PERCENTAGE = '100'
FILE_SIZE = '65536k'

KILLED_SERVER ='null                  22% |******                         | 14538k 00:00:10 ETA'
CONCATENATED = 'null                  52% |****************               | 34564k 00:00:05 ETAwget: read error: Connection timed out'
ERROR_ONLY = """
Connecting to 192.168.20.51:8000 (192.168.20.51:8000)

wget: can't connect to remote host (192.168.20.51): No route to host




"""
APE_LOG='null                  99% |****************************** |  1021M 00:00:00 ETA^Mnull                 100% |*******************************|  1024M 00:00:00 ETA'


class TestBusyboxWget(unittest.TestCase):
    def setUp(self):
        self.url = 'http://' + "".join([random.choice(string.letters) for ch in range(10)])
        self.connection = MagicMock()
        self.timeout = random.randint(1,100)
        self.destination = ''.join([random.choice(string.letters) for ch in range(random.randint(1,100))])
        self.logger = MagicMock()
        self.wget = BusyboxWget(url=self.url,
                                connection=self.connection,
                                timeout=self.timeout,
                                destination=self.destination)
        # change this to None to use logger-debugging
        self.wget._logger = self.logger
        return
        
    def test_constructor(self):
        "Does it set the expected values?"
        self.assertEqual(self.url, self.wget.url)
        self.assertEqual(self.connection, self.wget.connection)
        self.assertEqual(self.timeout, self.wget.timeout)
        self.assertEqual(self.destination, self.wget.destination)
        return

    def test_arguments(self):
        """
        Does it construct the proper argument string?
        """
        expected = 'wget {url} -O {destination} -T {timeout}'.format(url=self.url,
                                                                     destination=self.destination,
                                                                     timeout=self.timeout)
        actual = self.wget.arguments
        self.assertEqual(expected, actual)
        return

    def test_expression(self):
        """
        Does the expression extract the data?
        """
        match = self.wget.expression.search(COMPLETED_LINE)
        self.assertIsNotNone(match)
        destination = match.group(BusyboxEnum.destination)
        self.assertEqual(DESTINATION, destination)
        self.assertEqual(PERCENTAGE, match.group(BusyboxEnum.percentage_completed))
        self.assertEqual(FILE_SIZE, match.group(BusyboxEnum.kbits_transferred))
        return

    def test_killed_server(self):
        """
        Does the expression match if the server dies?
        """
        match = self.wget.expression.search(KILLED_SERVER)
        self.assertEqual('null', match.group(BusyboxEnum.destination))
        self.assertEqual('22', match.group(BusyboxEnum.percentage_completed))
        self.assertEqual('14538k', match.group(BusyboxEnum.kbits_transferred))
        return

    def test_run(self):
        """
        Does the run execute the correct sequence?
        """
        self.connection.busybox.return_value = SAMPLE, StringIO('')
        time_time = MagicMock()
        times = [3,1]
        def time_effects():
            return times.pop()        
        time_time.side_effect = time_effects
        with patch('time.time', time_time):
            data = self.wget.run()
        self.assertEqual(2, data.elapsed)
        self.assertEqual('100', data.percentage)
        self.assertEqual('65536k', data.kbits)
        self.assertEqual('', data.error)
        self.connection.busybox.assert_called_with('wget {0} -O {1} -T {2}'.format(self.url,
                                                                                   self.destination,
                                                                                   self.timeout),
                                                                                   timeout=1)
        return

    def test_error_string(self):
        """
        Does it work with partial transfers
        """
        self.connection.busybox.return_value = StringIO(CONCATENATED), StringIO('')
        start = 0
        end = 1347
        times = [end, start]
        time_effects = lambda : times.pop()
        time_time = MagicMock()
        time_time.side_effect = time_effects
        with patch('time.time', time_time):
            data = self.wget.run()
        self.assertEqual('52', data.percentage)
        self.assertEqual('34564k', data.kbits)
        self.assertEqual('Connection timed out', data.error)
        self.assertEqual(end-start, data.elapsed)
        return

    def test_error_only(self):
        "Does it still return a BusyboxWgetData tuple even if there was no transfer?"
        self.connection.busybox.return_value = StringIO(ERROR_ONLY), StringIO('')
        # mock the time.time calls
        start = random.randint(0,100)
        end = random.randint(0,100)
        times = [end, start]
        time_effects = lambda : times.pop()
        time_time = MagicMock()
        time_time.side_effect = time_effects
        with patch('time.time', time_time):
            data = self.wget.__call__()
        self.assertEqual('No route to host', data.error)
        self.assertEqual(NA, data.percentage)
        self.assertEqual(NA, data.kbits)
        self.assertEqual(end-start, data.elapsed)
        return

    def test_data_string(self):
        "Does the enum data-string match the expectation?"
        random_string = lambda x:  ''.join([random.choice(string.letters) for ch in range(random.randint(1,x))])
        error = random_string(10)
        percentage = random_string(2)
        kbits = random_string(5)
        elapsed = random_string(100)
        data = BusyboxWgetData(elapsed=elapsed,
                               error=error,
                               percentage=percentage,
                               kbits=kbits)
        self.assertEqual(",".join([elapsed,percentage,kbits,error]),
                         str(data))
        return

    def test_ape_string(self):
        '''
        Can it get data from an actual output string from the log?
        '''
        self.connection.busybox.return_value = StringIO(APE_LOG), StringIO('')
                # mock the time.time calls
        start = random.randint(0,100)
        end = random.randint(0,100)
        times = [end, start]
        time_effects = lambda : times.pop()
        time_time = MagicMock()
        time_time.side_effect = time_effects
        with patch('time.time', time_time):
            data = self.wget.__call__()
        self.assertEqual(data.percentage, '100')


if __name__ == "__main__":
    connection = MagicMock()
    wget = BusyboxWget('abc', connection)
    connection.busybox.return_value = StringIO(APE_LOG), StringIO('')#
    import pudb;pudb.set_trace()
    data = wget.__call__()
