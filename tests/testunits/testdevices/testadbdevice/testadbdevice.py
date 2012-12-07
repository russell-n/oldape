from unittest import TestCase

from mock import MagicMock
from nose.tools import raises

from apetools.devices import adbdevice

LOG_MESSAGE = "how now frau cow"

class AdbDeviceTest(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.adbdevice = adbdevice.AdbDevice(self.connection)
        return


    def test_log(self):
        self.adbdevice.log(LOG_MESSAGE)
        self.connection.log.assert_called_with(LOG_MESSAGE)
        return
    

# end class AdbDeviceTest
