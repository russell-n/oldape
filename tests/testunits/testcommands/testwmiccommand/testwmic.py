from unittest import TestCase

from mock import MagicMock

from apetools.commands import wmic
from apetools.commons import errors
from apetools.connections.nonlocalconnection import OutputError

PASS = """
Executing (\\IGOR\root\cimv2:Win32_NetworkAdapter.DeviceID="11")->enable()
Method execution successful.
Out Parameters:
instance of __PARAMETERS
{
        ReturnValue = 0;
};
""".split('\n')

PASS_LINE = "        ReturnValue = 0;"

FAIL = """
Executing (\\IGOR\root\cimv2:Win32_NetworkAdapter.DeviceID="11")->enable()
Method execution successful.
Out Parameters:
instance of __PARAMETERS
{
        ReturnValue = 5;
};
""".split('\n')

UNKNOWN = "No Instance(s) Available.".split('\n')

FAIL_LINE = "        ReturnValue = 5;"

BASE = "path Win32_NetworkAdapter where NetConnectionID='\"Wireless Network Connection\"' call {0}"

class TestWmic(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.enum= wmic.WmicEnumeration
        self.wmic = wmic.WmicWin32NetworkAdapter(connection=self.connection)
        return

    def test_expression(self):
        match = self.wmic.return_expression.search(PASS_LINE)
        self.assertEqual('0', match.groupdict()[self.enum.code])
        return

    def test_enable(self):
        self.wmic.enable_wifi()
        self.connection.wmic.assert_called_with(BASE.format("enable"))
        return

    def test_disable(self):
        self.wmic.disable_wifi()
        self.connection.wmic.assert_called_with(BASE.format("disable"))
        return
            
    def test_failure(self):
        self.connection.wmic.return_value = OutputError(FAIL, "")
        self.assertRaises(errors.CommandError, self.wmic.enable_wifi)
        return

    def test_unknown_interface(self):
        self.connection.wmic.return_value = OutputError(UNKNOWN, "")
        self.assertRaises(errors.CommandError, self.wmic.enable_wifi)
        return
# TestWmic
