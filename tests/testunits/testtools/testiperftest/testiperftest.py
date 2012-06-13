# python
from unittest import TestCase

# third party
from mock import MagicMock


from tottest.tools import iperftest


class IperfTestTest(TestCase):
    def setUp(self):
        self.sender = MagicMock()
        self.receiver = MagicMock()
        self.senderkill = MagicMock()
        self.receiverkill = MagicMock()
        self.parameters = MagicMock()
        self.sleep = MagicMock()
        self.iperftest = iperftest.IperfTest(sender=self.sender,
                                             receiver=self.receiver,
                                             killers = [self.senderkill, self.receiverkill], 
                                             sleep=self.sleep)
        return

    def test_run(self):
        self.parameters.recovery_time.return_value = 5
        self.iperftest.run(self.parameters)
        
        self.senderkill.run.assert_called_with(time_to_sleep=self.parameters.recovery_time)
        self.receiverkill.run.assert_called_with(time_to_sleep=self.parameters.recovery_time)
        self.receiver.start.assert_called_with(self.parameters.receiver)
        self.sleep.run.assert_called_with(self.parameters.recovery_time)
        self.sender.run.assert_called_with(self.parameters.sender)
