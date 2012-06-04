# python
from unittest import TestCase

# third party
from mock import MagicMock, call


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
        self.iperftest.run(self.parameters)
        self.senderkill.run.assert_called_with()
        self.receiverkill.run.assert_called_with()
        self.receiver.start.assert_called_with(self.parameters.receiver)
        self.sleep.run.assert_called_with(self.parameters.sleep)
        self.sender.run.assert_called_with(self.parameters.sender)
