"""
An operator operates tests.
"""
#python Libraries
from collections import namedtuple

# tottest Libraries
from tottest.baseclass import BaseClass
from countdowntimer import CountdownTimer
from tottest.tools import sleep
from tottest.commons import errors

TIME_REMAINING = "Estimated time Remaining: {t}"

OperatorStaticTestParameters = namedtuple("OperatorStaticTestParameters",
                                          ['operator_parameters',
                                           'static_parameters',
                                           'test_parameters'])

OperatorParameters = namedtuple("OperatorParameters", ['setup',
                                                       'teardown',
                                                       'test',
                                                       'device',
                                                       'watchers',
                                                       'cleanup'])

TEST_PREAMBLE = "**** ALLION: Starting Repetition {r} of {t} ****"
TEST_POSTAMBLE = "**** ALLION: Ending test - elapsed time = {t} ****"
TEST_RESULT = "**** ALLION: Time to Ping = {t} ****"

class TestOperator(BaseClass):
    """
    An operator runs the sequence of operations.
    """
    def __init__(self, parameters, *args, **kwargs):
        """
        :params:

         - `parameters`: OperatorStaticTestParameters object
        """
        super(TestOperator, self).__init__(*args, **kwargs)
        self.test_parameters = parameters.test_parameters
        self.parameters = parameters.operator_parameters
        self.static_parameters = parameters.static_parameters
        self._countdown_timer = None
        self._setup = None
        self._test = None
        self._teardown = None
        self._device = None
        self._watchers = None
        self._sleep = None
        self._cleanup = None
        return

    @property
    def sleep(self):
        """
        """
        if self._sleep is None:
            self._sleep = sleep.Sleep()
        return self._sleep

    @property
    def countdown_timer(self):
        """
        :return: a CountdownTimer
        """
        if self._countdown_timer is None:
            self._countdown_timer = CountdownTimer(self.static_parameters.repetitions)
        return self._countdown_timer

    @property
    def device(self):
        """
        :rtype: DeviceLog
        :return: device log from parameters
        """
        if self._device is None:
            self._device  = self.parameters.device
        return self._device

    @property
    def setup(self):
        """
        :return: The setup object from self.parameters.setup
        """
        if self._setup is None:
            self._setup = self.parameters.setup
        return self._setup

    @property
    def test(self):
        """
        :return: The test to run.
        """
        if self._test is None:
            self._test = self.parameters.test
        return self._test

    @property
    def teardown(self):
        """
        :return: parameters.teardown
        """
        if self._teardown is None:
            self._teardown = self.parameters.teardown
        return self._teardown

    @property
    def watchers(self):
        if self._watchers is None:
            self._watchers = self.parameters.watchers
        return self._watchers

    @property
    def cleanup(self):
        if self._cleanup is None:
            self._cleanup = self.parameters.cleanup
        return self._cleanup
    
    def _log_message(self, message):
        """
        Send message to running-code log and device log.
        """
        self.logger.info(message)
        self.device.log(message)
        return

    def one_repetition(self, parameter):
        """
        Holds the test algorithm for one repetition.

        This was moved out to make the exception handline cleaner.
        """
        self.logger.debug("Running Parameters: {0}".format(parameter))
        self._log_message(TEST_PREAMBLE.format(r=parameter.repetition,
                                               t=parameter.repetitions))
        self.setup.run(parameter)
        elapsed_time = self.test.run(parameter)
        self._log_message(TEST_RESULT.format(t=elapsed_time))
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

            self._log_message(TEST_POSTAMBLE.format(t=self.countdown_timer.total_time))
        except errors.ConnectionError as error:
            self.logger.error(error)
        finally:
            self.logger.info("Sleeping to let the logcat finish recording the test-information")
            self.sleep.run()
            self.watchers.stop()
            self.cleanup.run()
        return
# end TestOperator
