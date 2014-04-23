
# python standard library
import time
# this package
from apetools.baseclass import BaseClass
from apetools.commons.errors import ConfigurationError
from apetools.commands.busyboxwget import BusyboxWget, HEADER


class BusyboxWgetSession(BaseClass):
    """
    A busybox-based wget monitor
    """
    def __init__(self, url, connection, storage, repetitions=None,
                 data_file=None, recovery_time=1,
                 max_time=None):
        """
        BusyboxWgetSession constructor

        :param:

         - `url`: URL of server (http://<ip>[:<port>]/<file>)
         - `connection`: connection to device to run `wget`
         - `storage`: A file-like object to send data to
         - `repetitions`: number of times to call wget
         - `max_time`: maximum seconds to run
         - `data_file`: name to use for file
         - `recovery_time`: seconds to sleep if an error is detected
        """
        super(BusyboxWgetSession, self).__init__()
        self.url = url
        self.connection = connection
        self.storage = storage
        self.repetitions = repetitions
        self.max_time = max_time
        self.recovery_time = recovery_time
        self._data_file = data_file
        self.end_time = None
        self.increment = 1
        self.count = 0
        self._time_remains = False
        self._wget = None
        return

    @property
    def wget(self):
        """
        A busy box wget command
        """
        if self._wget is None:
            self._wget = BusyboxWget(url=self.url,
                                     connection=self.connection)
        return self._wget
    

    @property
    def data_file(self):
        """
        Name to use for data-file
        """
        if self._data_file is None:
            self._data_file = 'wget.csv'
        return self._data_file

    @property
    def time_remains(self):
        """
        Checks if time is remaining

         - increments self.count by self.increment
         - returns True if count <= repetitions
         
        """
        self.count += self.increment
        if self.max_time is not None:
            # False if count is too high or time has expired
            return all((self.count <= self.repetitions, time.time() < self.end_time))
        # False if count too high, regardless of time
        return self.count <= self.repetitions

    def start_timer(self):
        """
        Initializes the timer

        :raises: ConfigurationError if neither max_time nor repetitions set
        """
        self.count = 0
        if not any((self.max_time, self.repetitions)):
            raise ConfigurationError('max_time or repetitions need to be set')
        if self.repetitions is None:
            # make it so it can't run out
            self.repetitions = 1
            self.increment = 0            
        else:
            self.increment = 1
        if self.max_time not in (0,None) :
            # end-time is the time to stop
            self.end_time = time.time() + self.max_time
        else:
            # give the time_remaining a flag to know not to use time
            self.end_time = self.max_time = None            
        return

    def __call__(self, parameters=None, filename_prefix=None):
        """
        calls wget  until we are out of time or repetitions

        :param:

         - `parameters`: not used (legacy signature)
        """
        self.logger.info("Starting `wget` session")
        output = self.storage.open(self.data_file)
        output.write(HEADER)
        self.start_timer()
        while self.time_remains:
            self.logger.info('calling wget')
            data = self.wget()
            self.logger.info("{0}\n".format(data))
            output.write("{0}\n".format(data))
            if len(data.error):
                self.logger.error(data.error)
                self.logger.info('Sleeping for {0} second to allow for a recovery'.format(self.recovery_time))
                time.sleep(self.recovery_time)
        self.logger.info("Ended `wget` session")
        return


# python standard-library
import unittest
import random
import string
from StringIO import StringIO

# third-party
from mock import MagicMock, patch, call

#this package
from apetools.commands.busyboxwget import BusyboxWgetData


def random_string(maximum=100):
    return "".join([random.choice(string.letters) for ch in range(random.randint(0, maximum))])

class TestBusyboxWgetSession(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.storage = MagicMock()
        self.url = random_string(20)
        self.repetitions = 1
        self.max_time = 10
        self.session = BusyboxWgetSession(url=self.url,
                                          connection=self.connection,
                                          storage=self.storage,
                                          repetitions=self.repetitions,
                                          max_time=self.max_time)
        return

    def test_constructor(self):
        """
        Does the constructor match expectations?
        """
        self.assertEqual(self.connection, self.session.connection)
        self.assertEqual(self.url, self.session.url)
        self.assertEqual(self.storage, self.session.storage)
        self.assertEqual(self.repetitions, self.session.repetitions)
        self.assertEqual(self.max_time, self.session.max_time)
        return

    def test_call(self):
        """
        Does the call run the correct algorithm?
        """
        error = random_string()
        percentage = random.randint(0, 100)
        kbits = random.randint(0,10000)
        elapsed = random.randint(1,10)
        wget = MagicMock()
        wget.return_value = BusyboxWgetData(error=error,
                                            percentage=percentage,
                                            kbits=kbits,
                                            elapsed=elapsed)
        self.session._wget = wget
        self.session.max_time = 0
        reps = random.randint(0,100)
        self.session.repetitions = reps
        out_file = MagicMock()
        self.storage.open.return_value = out_file
        self.session()
        self.assertIsNone(self.session.end_time)
        calls = [call.write(HEADER)] + [call.write("{0}\n".format(wget.return_value))] * reps
        self.assertEqual(calls, out_file.mock_calls)
        return

    def test_start_timer(self):
        """
        Does the start_timer method set up the stopping conditions?
        """
        self.session.max_time = 0
        self.session.repetitions = None
        self.assertRaises(ConfigurationError, self.session.start_timer)

        # set end-time, disable increment counter
        self.session.max_time = 1
        time_time = MagicMock()
        times = [1]
        time_effects = lambda : times.pop()
        time_time.side_effect = time_effects
        with patch('time.time', time_time):
            self.session.start_timer()
        self.assertEqual(self.session.end_time, 2)
        self.assertEqual(self.session.repetitions, 1)
        self.assertEqual(self.session.increment, 0)
        self.assertEqual(self.session.count, 0)

        # time and repetitions set
        reps = random.randint(1,100)
        self.session.repetitions = reps
        max_time = random.randint(1,100)
        self.session.max_time = max_time
        time = random.randint(1,100)
        times = [time]
        with patch('time.time', time_time):
            self.session.start_timer()
        self.assertEqual(self.session.end_time, max_time + time)
        self.assertEqual(self.session.repetitions, reps)
        self.assertEqual(self.session.increment,1)        

        # time not set, repetitions are
        self.session.max_time = 0
        time = random.randint(1,100)
        times = [time]
        with patch('time.time', time_time):
            self.session.start_timer()
        self.assertEqual(self.session.end_time, None)
        self.assertEqual(self.session.repetitions, reps)
        self.assertEqual(self.session.increment,1)
        return

    def test_time_remains(self):
        """
        Does time_remains return True at the correct time?
        """
        # repetitions only
        self.session.max_time = 0
        reps = random.randint(1,100)
        self.session.repetitions = reps
        self.session.start_timer()
        for rep in range(reps):
            self.assertTrue(self.session.time_remains)
        self.assertFalse(self.session.time_remains)

        # time only
        self.session.repetitions = None
        max_time = random.randint(1,100)
        self.session.max_time = max_time
        time_time = MagicMock()

        # times is a collection if times less than max time except for the last value
        # if first time.time is 0, end_time is max_time
        # need max_time 0's to handle start_timer call
        times = [max_time + 1] + [0 for i in range(max_time+1)]
        
        time_effects = lambda : times.pop()
        time_time.side_effect = time_effects
        with patch('time.time', time_time):
            self.session.start_timer()
            self.assertEqual(self.session.increment, 0)
            self.assertEqual(self.session.count, 0)
            self.assertEqual(self.session.repetitions, 1)
            self.assertEqual(self.session.end_time, self.session.max_time)

            for rep in range(max_time):
                self.assertTrue(self.session.time_remains)
            self.assertFalse(self.session.time_remains)

        # time and repetitions
        reps = random.randint(1,100)
        max_time = random.randint(1,100)
        times = [max_time + 1] + [0 for t in range(max_time + 1)]
        time_effects = lambda: times.pop()
        time_time.side_effect = time_effects
        self.session.repetitions = reps
        self.session.max_time = max_time
        with patch('time.time', time_time):
            self.session.start_timer()
            for t in range(min(reps, max_time)):
                self.assertTrue(self.session.time_remains)
            self.assertFalse(self.session.time_remains)
        return

    def test_wget(self):
        """
        Does the session create a wget?
        """
        self.session._wget = None
        self.assertIsInstance(self.session.wget, BusyboxWget)
        self.assertEqual(self.url,self.session.wget.url)
        self.assertEqual(self.connection, self.session.wget.connection)
        return