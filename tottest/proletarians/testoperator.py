"""
An operator operates tests.
"""
#python Libraries
from collections import namedtuple
from Queue import Queue

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.tools import sleep
from tottest.commons import errors


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
    def __init__(self, test_parameters, operation_setup, operation_teardown,
                 test_setup, tests, test_teardown,
                 countdown_timer, sleep=None):
        """
        :params:

         - `test_parameters`: A generator of test parameters
         - `operation_setup`: A set up to run before (all) the tests
         - `operation_teardown`: A TearDown to run after (all) the tests
         - `test_setup`: A set up to run before each test
         - `tests`: The tests to be run with each parameter subset
         - `test_teardown`: A tear down to run after each test is run
         - `countdown_timer`: An estimator of remaining time
         - `sleep`: A sleep for recovery times
        """
        super(TestOperator, self).__init__()
        self.test_parameters = test_parameters
        self.operation_setup = operation_setup
        self.operation_teardown = operation_teardown
        self.test_setup = test_setup
        self.tests = tests
        self.test_teardown = test_teardown
        self.countdown_timer = countdown_timer
        self._sleep = sleep
        self.parameter_queue = Queue()
        return

    @property
    def sleep(self):
        """
        :return: default Sleep object
        """
        if self._sleep is None:
            self._sleep = sleep.Sleep()
        return self._sleep
        
    def one_repetition(self, parameter, count):
        """
        Holds the test algorithm for one repetition.

        This was moved out to make the exception handling cleaner.

        #. Runs Setup
        #. Runs test
        #. Runs Teardown
        """
        self.logger.info("Running Parameters: {0}".format(parameter))
        self.logger.info(TEST_PREAMBLE.format(r=count,
                                              t=parameter.total_count))
        self.logger.info("Running test setup")
        #import pudb; pudb.set_trace()
        self.test_setup(parameter)
        self.sleep()
        
        self.logger.info("Running Test")
        test_result = self.tests(parameter)
        self.logger.info(TEST_RESULT.format(r=test_result))
        self.logger.info("Running teardown")
        self.test_teardown(parameter)
        self.logger.info(TIME_REMAINING.format(t=self.countdown_timer()))
        return
    
    def run(self):
        """
        This is the main operation method.
        """
        self.operation_setup()
        self.countdown_timer()
        try:
            count = 0
        
            for parameter in self.test_parameters:
                count += 1
                try:
                    self.one_repetition(parameter, count)
                except (errors.AffectorError, errors.CommandError) as error:
                    self.logger.error(error)
                    self.logger.error("Quitting this iteration")
                    self.parameter_queue.put(parameter)
                    count -= 1
                    
            while not self.parameter_queue.empty():
                parameter = self.parameter_queue.get()
                self.logger.info("Re-trying: {0}".format(parameter))
                count += 1
                try:
                    self.one_repetition(parameter, count)
                except (errors.AffectorError, errors.CommandError) as error:
                    self.logger.error(error)
                    self.logger.error("Quitting this iteration")
                
            self.logger.info(TEST_POSTAMBLE.format(t=self.countdown_timer.total_time))
            self.logger.info("Sleeping to let the logs finish recording the test-information")
            self.sleep()
        except (errors.ConnectionError, errors.CommandError, errors.ConfigurationError) as error:
            self.logger.error(error)
        finally:
            self.operation_teardown()
        return
# end TestOperator
