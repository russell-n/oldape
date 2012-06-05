from unittest import TestCase

from nose.tools import raises
from mock import MagicMock, call

from tottest.tools import setupiteration
from tottest.commons import errors

from iw_link import output

ConfigurationError = errors.ConfigurationError


class SetupIterationTest(TestCase):
    def setUp(self):
        self.device = MagicMock()
        self.device.get_wifi_info.return_value = output
        self.affector = MagicMock()
        self.time_to_recovery = MagicMock()
        self.time_to_recovery.run.return_value = 10
        self.sleep = MagicMock()
        self.parameters = MagicMock()
        self.parameters.ap.return_value = 2
        self.parameters.recovery_time = 5
        self.setupiteration = setupiteration.SetupIteration(device=self.device,
                                                            affector=self.affector,
                                                            time_to_recovery=self.time_to_recovery)
        self.setupiteration._sleep = self.sleep
        return

    def test_run(self):
        self.setupiteration.run(self.parameters)
        self.affector.run.assert_called_with(self.parameters.ap)
        self.time_to_recovery.run.assert_called_with()
        calls = [call("Time to recovery: 10"), call(output)]
        self.assertEqual(self.device.log.mock_calls, calls)
        self.sleep.run.assert_called_with(5)
        return

    @raises(ConfigurationError)
    def test_fail(self):
        self.time_to_recovery.run.return_value = None
        self.setupiteration.run(self.parameters)
        return
# end class SetupIteration
