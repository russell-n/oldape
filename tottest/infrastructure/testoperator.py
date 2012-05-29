"""
An operator operates tests.
"""
#python Libraries
from collections import namedtuple

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.tools import sleep
from tottest.commons import errors

TIME_REMAINING = "Estimated time Remaining: {t}"

OperatorStaticTestParameters = namedtuple("OperatorStaticTestParameters",
                                          ['operator_parameters',
                                           'static_parameters',
                                           'test_parameters'])


TEST_PREAMBLE = "**** ALLION: Starting Repetition {r} of {t} ****"
TEST_POSTAMBLE = "**** ALLION: Ending test - elapsed time = {t} ****"
TEST_RESULT = "**** ALLION: Test Result = {r} ****"

class TestOperator(BaseClass):
    """
    An operator runs the sequence of operations.
    """
    def __init__(self, setup, teardown, test, device, watchers, cleanup,
                 countdown_timer, sleep=None):
        """
        :params:

         - `setup`: A SetUp to run for each repetition
         - `teardown`: A TearDown to run for each repetition
         - `test`: A test to run between setup and teardown
         - `device`: A device to send log messages to
         - `watcher`: threaded watchers to start
         - `cleanup`: A CleanUp to run after all the tests are done
         - `countdown_timer`: An estimator of remaining time
         - `sleep`: A sleep for recovery times
        """
        super(TestOperator, self).__init__()
        self.setup = setup
        self.teardown = teardown
        self.test = test
        self.device = device
        self.watchers = watchers
        self.cleanup = cleanup
        self.countdown_timer = countdown_timer
        self._sleep = sleep
        return

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

    def one_repetition(self, parameter):
        """
        Holds the test algorithm for one repetition.

        This was moved out to make the exception handling cleaner.

        #. Runs Setup
        #. Runs test
        #. Runs Teardown
        """
        self.logger.debug("Running Parameters: {0}".format(parameter))
        self.log_message(TEST_PREAMBLE.format(r=parameter.repetition,
                                               t=parameter.repetitions))
        self.setup.run(parameter)
        test_result = self.test.run(parameter)
        self.log_message(TEST_RESULT.format(r=test_result))
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
                self.one_repetition(parameter)

            self.log_message(TEST_POSTAMBLE.format(t=self.countdown_timer.total_time))
        except errors.ConnectionError as error:
            self.logger.error(error)
        finally:
            self.logger.info("Sleeping to let the logs finish recording the test-information")
            self.sleep.run()
            self.watchers.stop()
            self.cleanup.run()
        return
# end TestOperator
