from unittest import TestCase
from mock import MagicMock

from tottest.devices.linuxdevice import LinuxDevice

class TestLinuxDevice(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.device = LinuxDevice(self.connection)
        return

    def test_ip_address(self):
        return
# end TestLinuxDevice
