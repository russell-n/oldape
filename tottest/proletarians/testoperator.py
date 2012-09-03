"""
An operator operates tests.
"""
#python Libraries
from collections import namedtuple

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.tools import sleep
from tottest.commons import errors

# another last minute hack for amazon
from tottest.connections.adbconnection import ADBConnection, ADBShellBlockingConnection

TIME_REMAINING = "Estimated time Remaining: {t}"

OperatorStaticTestParameters = namedtuple("OperatorStaticTestParameters",
                                          ['operator_parameters',
                                           'static_parameters',
                                           'test_parameters'])


TEST_PREAMBLE = "**** ALLION: Repetition {r} of {t} ****"
TEST_POSTAMBLE = "**** ALLION: Ending test - elapsed time = {t} ****"
TEST_RESULT = "**** ALLION: Test Result = {r} ****"

class TestOperator(BaseClass):
    """
    An operator runs the sequence of operations.
    """
    def __init__(self, test_parameters, setup, teardown, tests, device, watchers,
                 cleanup, countdown_timer, sleep=None):
        """
        :params:

         - `test_parameters`: A generator of test parameters
         - `setup`: A SetUp to run for each repetition
         - `teardown`: A TearDown to run for each repetition
         - `tests`: A dictionary of test_id:test where tests are to be run
         - `device`: A device to send log messages to
         - `watcher`: threaded watchers to start
         - `cleanup`: A CleanUp to run after all the tests are done
         - `countdown_timer`: An estimator of remaining time
         - `sleep`: A sleep for recovery times
        """
        super(TestOperator, self).__init__()
        self.test_parameters = test_parameters
        self.setup = setup
        self.teardown = teardown
        self.tests = tests
        self.device = device
        self.watchers = watchers
        self.cleanup = cleanup
        self.countdown_timer = countdown_timer
        self._sleep = sleep
        self._adb_connection = None
        self._adb_blocking_shell = None
        return

    @property
    def adb_connection(self):
        if self._adb_connection is None:
            self._adb_connection = ADBConnection()
        return self._adb_connection

    @property
    def adb_blocking_shell(self):
        if self._adb_blocking_shell is None:
            self._adb_blocking_shell = ADBShellBlockingConnection()
        return self._adb_blocking_shell

    @property
    def sleep(self):
        """
        :return: default Sleep object
        """
        if self._sleep is None:
            self._sleep = sleep.Sleep()
        return self._sleep
        
    def log_message(self, message):
        """
        Send message to running-code log and device log.
        """
        self.logger.info(message)
        self.device.log(message)
        return

    def reboot(self):
        self.adb_connection.reboot()
        output, error = self.adb_blocking_shell.bugreport()
        for line in output:
            self.logger.info(line)
        for line in error:
            self.logger.error(line)
        return

    def one_repetition(self, parameter):
        """
        Holds the test algorithm for one repetition.

        This was moved out to make the exception handling cleaner.

        #. Runs Setup
        #. Runs test
        #. Runs Teardown
        """
        self.logger.info("Running Parameters: {0}".format(parameter))
        test = self.tests[parameter.test_id]
        self.log_message(TEST_PREAMBLE.format(r=parameter.repetition,
                                               t=parameter.repetitions))
        self.logger.info("Running test setup")
        self.setup.run(parameter)
        self.logger.info("Running Test")
        test_result = test.run(parameter)
        self.log_message(TEST_RESULT.format(r=test_result))
        self.logger.info("Running teardown")
        self.teardown.run(parameter)
        self.logger.info(TIME_REMAINING.format(t=self.countdown_timer.remaining_time))
        return
    
    def run(self):
        """
        This is the main operation method.
        """
        self.watchers.start()
        self.countdown_timer.start_timer()
        
        try:
            for parameter in self.test_parameters:
                try:
                    self.one_repetition(parameter)
                except (errors.AffectorError, errors.CommandError) as error:
                    self.logger.error(error)
                    self.logger.error("Quitting this iteration")
                    
            self.log_message(TEST_POSTAMBLE.format(t=self.countdown_timer.total_time))
            self.logger.info("Sleeping to let the logs finish recording the test-information")
            self.sleep.run()
        except (errors.ConnectionError, errors.CommandError, errors.ConfigurationError) as error:
            self.logger.error(error)
        finally:
            self.watchers.stop()
            self.cleanup.run()
        return
# end TestOperator
