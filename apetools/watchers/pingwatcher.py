
# python standard library
import re
import time
from collections import namedtuple

# this package
from apetools.baseclass import BaseThreadClass
from apetools.commons.errors import CommandError
from apetools.commons import expressions
from apetools.commons.enumerations import OperatingSystem
from apetools.threads import threads
from apetools.commons.timestamp import TimestampFormat, TimestampFormatEnums
from apetools.commands.ping import PingArguments


HEADER = 'TimeOfEvent,Event,SecondsToEvent\n'
ADD_NEWLINE = '{0}\n'


class FailureData(namedtuple('FailureData', 'timestamp elapsed'.split())):
    """
    A tuple to hold Failure Data
    """
    event = 'Failure'
    __slots__ = ()
    def __str__(self):
        """
        Returns 'timestamp,event,elapsed'
        """
        return "{0},{1},{2}".format(self.timestamp, self.event, self.elapsed)


class RecoveryData(FailureData):
    """
    Holds recovery event data
    """
    event = 'Recovery'


class PingWatcher(BaseThreadClass):
    """
    A PingWatcher monitors pings and records times to failure(s)

    """
    def __init__(self, target, output, connection, threshold=5,
                 event=None, interval=1,
                 timestamp_format=TimestampFormatEnums.log,
                 *args, **kwargs):
        """
        Pingwatcher constructor
        
        :param:

         - `target`: hostname to ping
         - `output`: A file-like object to send output to.
         - `threshold`: consecutive ping-failures to count as a failure
         - `interval`: time between pings
         - `event`: A threading event to stop a threaded watcher
         - `connection`: A connection to the Device         
         - `timestamp_format`: One of the TimestampFormatEnums
        """
        super(PingWatcher, self).__init__(*args, **kwargs)
        self.target = target
        self.output = output        
        self.event = event
        self.connection = connection
        self.threshold = int(threshold)
        self.interval = float(interval)
        self._arguments = None
        self.timestamp_format = timestamp_format
        self._timestamp = None
        self._logger = None
        self._expression = None
        self._stop = None
        self._stopped = None
        return

    @property
    def arguments(self):
        """
        Command-line arguments for the `ping` command

        :return: argument string for ping
        """
        if self._arguments is None:
            self._arguments = (PingArguments.arguments[self.connection.operating_system] +
                               self.target)
        return self._arguments

    @property
    def expression(self):
        """
        Compiled regular expression to match a ping
        """
        if self._expression is None:
            self._expression = re.compile(expressions.PING)
        return self._expression
    
    @property
    def timestamp(self):
        """
        :return: a time-stamper
        """
        if self._timestamp is None:
            self._timestamp = TimestampFormat(self.timestamp_format)
        return self._timestamp

    @property
    def stop(self):
        """
        This sets the event (to match the Watcher).

        """
        if self.event is not None:
            #self.event.set()
            pass
        return 

    @property
    def stopped(self):
        """
        :rtype: Boolean
        :return: True if self.stop is set.
        """
        if self.event is not None:
            return self.event.is_set()
        return False

    def execute(self):
        """
        Calls the ping, generates the lines
        
        :yield:  lines from standard out
        """
        with self.connection.lock:
            output, error = self.connection.ping(self.arguments)
        for line in output:
            self.logger.debug(line)
            yield line
        err = error.readline()
        if len(err):
            self.logger.error(err)
        return

    def ping(self):
        """
        Executes as single ping and searches for the round-trip-time

        :return: rtt (as a string, no units) or None
        """
        lines = self.execute()
        
        for line in lines:
            match = self.expression.search(line)
            if match is not None:
                return match.group('rtt')
        return

    def time_to_event(self, event_evaluation, event_data):
        """
        Runs the ping, evaluates the outcome based on event evaluation

        :param:

         - `event_evaluation`: methods that returns True or False based on ping fail/success
         - `event_data`: RecoveryData or FailureData namedtuples
        """
        start_time = time.time()
        events = 0
        first_time = None
        while events < self.threshold and not self.stopped:
            loop_start = time.time()
            rtt = self.ping()
            if event_evaluation(rtt):
                events += 1
                if events == 1:
                    first_time = time.time()
                    first_timestamp = self.timestamp()
                    self.logger.debug('possible event-state change')
            else:
                events, first_time = 0, None
            loop_end = time.time()
            try:
                time.sleep(self.interval - (loop_end - loop_start))
            except IOError:
                self.logger.debug(("ping took {0} seconds (greater than {1} " +
                                   "second interval)").format(loop_end-loop_start,
                                                              self.interval))
        if events == self.threshold:
            return event_data(timestamp=first_timestamp, elapsed=first_time-start_time)
        return
    
    def run(self):
        """
        Runs an infinite loop that pings the target

        Writes changes in connectivity state to output

        """
        self.output.write(HEADER)
        while not self.stopped:            
            self.logger.debug('Waiting for a Failure')
            outcome = self.time_to_failure()
            if outcome:
                self.logger.info('PingWatch: Failure Detected')
                self.output.write(ADD_NEWLINE.format(outcome))
            outcome = self.time_to_recovery()
            if outcome:
                self.logger.info('PingWatch: Recovery Detected')
                self.output.write(ADD_NEWLINE.format(outcome))
        return
    
    def time_to_recovery(self):
        """
        runs until the connection pings successfully

        :return: RecoveryData
        """        
        return self.time_to_event(lambda rtt: rtt is not None,
                                  RecoveryData)

    def time_to_failure(self):
        """
        Runs until the connection fails to ping

        :return: FailureData
        """
        return self.time_to_event(lambda rtt: rtt is None,
                                  FailureData)

    def start(self):
        """
        Runs self in a thread.

        :rtype: threading.Thread        
        """
        self.thread =  threads.Thread(target=self.run_thread,
                                      name="PingWatcher {0}".format(self.arguments))
        return self.thread

    def __str__(self):
        return "ping {0}".format(self.arguments)
# end class PingWatcher


# python standard library
import unittest
from StringIO import StringIO
# third party
from mock import MagicMock, patch, call


example = '''
PING 192.168.20.1 (192.168.20.1) 56(84) bytes of data.
64 bytes from 192.168.20.1: icmp_seq=1 ttl=255 time=207 ms

--- 192.168.20.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 207.135/207.135/207.135/0.000 ms
'''

class TestPingWatcher(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        # set the operating system for the arguments
        self.connection.operating_system = OperatingSystem.android

        self.logger = MagicMock()
        self.event = MagicMock()
        self.output = MagicMock()
        self.target = '192.168.10.1'
        
        self.threshold = 1
        self.watcher=PingWatcher(target=self.target,
                                 output=self.output,
                                 connection=self.connection,
                                 threshold=self.threshold,
                                 event=self.event)
        self.watcher._logger = self.logger
        return

    def test_constructor(self):
        """
        Does the constructor set all the parameters we pass in?
        """
        self.assertEqual(self.target, self.watcher.target)
        self.assertEqual(self.output,self.watcher.output)
        self.assertEqual(self.connection, self.watcher.connection)
        self.assertEqual(self.threshold, self.watcher.threshold)
        self.assertEqual(self.event, self.watcher.event)
        return

    def test_arguments(self):
        """
        Does the argument-string get created correctly?
        """
        self.connection.operating_system = OperatingSystem.android
        self.assertEqual(" -c 1 -w 1 " + self.target, self.watcher.arguments)
        self.watcher._arguments = None
        self.connection.operating_system = OperatingSystem.linux
        self.assertEqual(' -c 1 -w 1 ' + self.target, self.watcher.arguments)
        return

    def test_expression(self):
        self.assertIsNotNone(self.watcher.expression.search(example))
        match = self.watcher.expression.search(example)
        self.assertEqual('207', match.group('rtt'))
        return

    def test_excecute(self):
        error = 'cow'
        self.connection.ping.return_value = example.split('\n'), StringIO(error)
        for line in self.watcher.execute():
            self.assertIn(line, example)
        self.logger.error.assert_called_with(error)
        return

    def test_ping(self):
        self.connection.ping.return_value = example.split('\n'), StringIO('')
        self.assertEqual('207', self.watcher.ping())
        error = 'asonetuh'
        self.connection.ping.return_value = '\n', StringIO(error)
        self.assertIsNone(self.watcher.ping())
        return
    
    def test_run(self):
        timestamp = MagicMock()
        self.watcher._timestamp = timestamp
        self.watcher._timestamp.return_value = 5
        self.connection.ping.return_value = '\n\n'.split('\n'), StringIO('')
        # prevent the infinite loop
        events = [True, True, False, False]
        def side_effects():
            return events.pop()
        self.event.is_set.side_effect = side_effects

        # set the times
        time_time = MagicMock()
        # the time_to_event checks the time once before checking is_stopped
        # so there needs to be 1 extra time
        times = [2,2,2,1,1]
        def time_effects():
            return times.pop()
        time_time.side_effect = time_effects
        
        with patch('time.time', time_time):
            self.watcher.run()
        time_time.assert_called_with()
        self.connection.ping.assert_called_with(self.watcher.arguments)
        calls = [call(HEADER), call('5,Failure,1\n')]
        self.assertEqual(calls, self.output.write.mock_calls)
        return
        
