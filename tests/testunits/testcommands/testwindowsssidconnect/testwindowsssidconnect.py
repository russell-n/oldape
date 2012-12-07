from unittest import TestCase
from StringIO import StringIO

from mock import MagicMock
from nose.tools import raises

from apetools.commons.errors import CommandError
from apetools.commands.windowsssidconnect import WindowsSSIDConnect

OUTPUT = """
Connection request was completed successfully.
"""

ERROR = """
There is no profile "Cisco29883" assigned to the specified interface.
"""


ERROR_2 = """
There is no wireless interface on the system.
"""

class TestWindowsSSIDConnect(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.command = WindowsSSIDConnect(self.connection)
        return

    def test_connect(self):
        self.connection.netsh.return_value = StringIO(OUTPUT), ""
        self.command("allionstaff")
        self.connection.netsh.assert_called_with('wlan connect name="allionstaff" ssid="allionstaff"')
        return
    
    @raises(CommandError)
    def test_error(self):
        self.connection.netsh.return_value = StringIO(ERROR), ""
        self.command("allionstaff")
        return

    @raises(CommandError)
    def test_wifi_disabled(self):
        self.connection.netsh.return_value = StringIO(ERROR_2), ""
        self.command("allionstaff")
# end class TestWindowsSSIDConnect
        
