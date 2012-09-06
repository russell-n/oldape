from unittest import TestCase

from mock import MagicMock
from nose.tools import raises

from tottest.devices import adbdevice

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
    
    @raises(NotImplementedError)
    def test_get_wifi_info(self):
        self.adbdevice.get_wifi_info()

    @raises(NotImplementedError)
    def test_enable_wifi(self):
        self.adbdevice.enable_wifi()

    @raises(NotImplementedError)
    def test_disable_wifi(self):
        self.adbdevice.disable_wifi()

    @raises(NotImplementedError)
    def test_display(self):
        self.adbdevice.display("")

    @raises(NotImplementedError)
    def test_wake_screen(self):
        self.adbdevice.wake_screen()
        return
# end class AdbDeviceTest
