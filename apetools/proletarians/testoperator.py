"""
An operator operates tests.
"""
#python Libraries
from collections import namedtuple
from Queue import Queue
import os
import sys
import signal

# apetools Libraries
from apetools.baseclass import BaseClass
from apetools.tools import sleep
from apetools.commons import errors
from apetools.commons import sublogger

TIME_REMAINING = "Estimated time Remaining: {t}"

OperatorStaticTestParameters = namedtuple("OperatorStaticTestParameters",
                                          ['operator_parameters',
                                           'static_parameters',
                                           'test_parameters'])


TEST_TAG = "**** ALLION: {s} Test {r} of {t} ****"

TEST_POSTAMBLE = "**** ALLION: Ending test - elapsed time = {t} ****"
TEST_RESULT = "**** ALLION: Test Result = {r} ****"

class TestOperator(BaseClass):
    """
    An operator runs the sequence of operations.
    """
    def __init__(self, test_parameters, operation_setup, operation_teardown,
                 test_setup, tests, test_teardown,nodes, no_cleanup,
                 countdown_timer, storage, sleep=None):
        """
        :params:

         - `test_parameters`: A generator of test parameters
         - `operation_setup`: A set up to run before (all) the tests
         - `operation_teardown`: A TearDown to run after (all) the tests
         - `test_setup`: A set up to run before each test
         - `tests`: The tests to be run with each parameter subset
         - `test_teardown`: A tear down to run after each test is run
         - `nodes`: a dictionary of nodes
         - `no_cleanup`: if True, allow ctrl-c to kill immediately
         - `countdown_timer`: An estimator of remaining time
         - `storage`: a storage-output (mainly to get the 
         - `sleep`: A sleep for recovery times
        """
        super(TestOperator, self).__init__()
        self.test_parameters = test_parameters
        self.operation_setup = operation_setup
        self.operation_teardown = operation_teardown
        self.test_setup = test_setup
        self.tests = tests
        self.test_teardown = test_teardown
        self.nodes = nodes
        self.no_cleanup = no_cleanup
        self.storage=storage
        self.countdown_timer = countdown_timer
        self._sleep = sleep
        self._sub_logger = None
        self.parameter_queue = Queue()
        return

    @property
    def sub_logger(self):
        """
        :return: holder of sub-logger
        """
        if self._sub_logger is None:
            self._sub_logger = sublogger.SubLogger()
        return self._sub_logger
    
    @property
    def sleep(self):
        """
        :return: default Sleep object
        """
        if self._sleep is None:
            self._sleep = sleep.Sleep()
        return self._sleep
        
    def one_repetition(self, parameter, count, prefix):
        """
        Holds the test algorithm for one repetition.

        This was moved out to make the exception handling cleaner.

        #. Runs Setup
        #. Runs test
        #. Runs Teardown

        :param:

         - `parameter`: namedtuple with tool-parameters
         - `count`: the current test-count (for logging)
         - `prefix`: any file-prefix given by the operation-setup
        """
        if prefix is not None:
            filename_prefix = prefix
        else:
            filename_prefix = ''
        #**** Setup Test
        self.logger.info("Running Parameters: {0}".format(parameter))
        message = TEST_TAG.format(r=count,
                                  t=parameter.total_count,
                                  s='Starting')
        self.log_info(message, parameter.nodes.parameters)
        self.logger.info("Running test setup")

        filename_prefix = "{0}_{1}".format(filename_prefix, self.test_setup(parameter))
        self.sleep()

        #**** Execute test
        self.logger.info("Running Test")
        test_result = self.tests(parameter, filename_prefix)
        self.logger.info(TEST_RESULT.format(r=test_result))
        self.logger.info("Running teardown")

        #**** Teardown Test
        self.test_teardown(parameter)
        self.logger.info(TIME_REMAINING.format(t=self.countdown_timer()))
        message = TEST_TAG.format(r=count,
                                  t=parameter.total_count,
                                  s='Ending')
        self.log_info(message, parameter.nodes.parameters)
        return

    def log_info(self, message, node):
        """
        :param:

         - `message`: a string to log
         - `node`: the name of the current node

        :postcondition: message sent to node and info log.
        """
        self.logger.info(message)
        self.nodes[node].log('"{0}"'.format(message))
        return
    
    def __call__(self):
        """
        This is the main operation method.
        """
        sublog_name = 'testoperation.log'
        sublog_name = self.storage.get_full_path(sublog_name)
        self.sub_logger.add(sublog_name)
        if self.no_cleanup:
            self.keyboard_interrupt_intercept()


        prefix = self.operation_setup()
        self.countdown_timer()
        try:
            count = 0        
            for parameter in self.test_parameters:
                count += 1
                try:
                    self.one_repetition(parameter, count, prefix)
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
                    self.one_repetition(parameter, count, prefix)
                except (errors.AffectorError, errors.CommandError) as error:
                    self.logger.error(error)
                    self.logger.error("Quitting this iteration")
                
            self.logger.info(TEST_POSTAMBLE.format(t=self.countdown_timer.total_time))
            self.logger.info("Sleeping to let the logs finish recording the test-information")
            self.sleep()
        except (errors.ConnectionError, errors.CommandError, errors.ConfigurationError) as error:
            self.logger.error(error)
        finally:
            self.logger.info("Tearing Down the Current Operation")
            self.operation_teardown()
            self.sub_logger.remove(logname=sublog_name)
        return

    def keyboard_interrupt_intercept(self):
        """
        The watcher watches for signal interrupts and kills children.

        This was implemented to prevent user-confusion when a ctrl-c is
        sent and the interpreter tries to clean up the threads
        """
        child = os.fork()
        if child == 0:
            return
        try:
            os.wait()
        except KeyboardInterrupt:
            self.logger.warning("Keyboard-Interrupt (killing without cleanup...)")
            os.kill(child, signal.SIGKILL)
        sys.exit()
        return

# end TestOperator
