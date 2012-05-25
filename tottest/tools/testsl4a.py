"""
A module to test the sl4a connection.
"""

from timetorecovertest.baseclass import BaseClass
from timetorecovertest.connections import adbconnection
from timetorecovertest.devices import sl4adevice
from timetorecovertest.commons import expressions

class TestSl4a(BaseClass):
    """
    TestSl4a tests the sl4a connection.
    """
    def __init__(self, parameters, *args, **kwargs):
        """
        :param:

         - `parameters`: an object with the wifi_interface attribute.
        """
        super(TestSl4a, self).__init__(*args, **kwargs)
        self.parameters = parameters
        self._adb_shell = None
        self._sl4a_device = None
        self._wifi_interface = None
        return

    @property
    def adb_shell(self):
        if self._adb_shell is None:
            self._adb_shell = adbconnection.ADBShellConnection()
        return self._adb_shell

    @property
    def sl4a_device(self):
        if self._sl4a_device is None:
            self._sl4a_device = sl4adevice.SL4ADevice()
        return self._sl4a_device

    @property
    def wifi_interface(self):
        if self._wifi_interface is None:
            self._wifi_interface = self.parameters.wifi_interface
        return self._wifi_interface

    def run(self):
        """
        Gets info from the device and puts it on the screen.
        """
        info = self.sl4a_device.get_wifi_info().replace(',', '\n')
        output = self.adb_shell.ifconfig(self.wifi_interface)
        for line in output:
            match = expressions.IP_ADDRESS.search(line)
            if match:
                info += '\nReal IP: ' + match.group()
                break
                
            self.logger.error("The IP Address could not be found. The Android doesn't appear to have an ip address or is using a different interface (not {0}).".format(self.wifi_interface))
            
        self.sl4a_device.display(info)
        print "*" * 40
        print info
        print "*"  * 40
        return
# end class TestSl4a

if __name__ == "__main__":
    from collections import namedtuple
    Param = namedtuple("Param", "wifi_interface")
    param = Param("wlan0")
    ts = TestSl4a(param)
    ts.run()
