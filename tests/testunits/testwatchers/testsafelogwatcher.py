from unittest import TestCase


from mock import MagicMock as Mock
from mock import call
from kmsg import output, output_copy
# apetools
from apetools.watchers import logwatcher

class SafeLogWatcherTest(TestCase):
    def setUp(self):
        self.mock = Mock()
        self.path = "/proc/kmsg"
        self.expected = output.split('\n')
        
        self.watcher = logwatcher.SafeLogWatcher(output=self.mock, arguments=self.path, connection=self.mock)
        return

    def test_run(self):
        self.mock.cat.return_value = self.expected, None
        #self.watcher._logger = self.mock
        self.watcher.run()

        expectation = [call.lock.__enter__(), call.cat(self.path), call.lock.__exit__(None, None, None)]

        for line in self.expected:
            expectation.append(call.write(line))        

        self.assertEqual(self.mock.mock_calls, expectation)
        return
