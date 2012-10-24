from unittest import TestCase

from mock import MagicMock

from tottest.connections import telnetconnection

DEFAULT_PATH = "/sys:/bin"


class TestLocalConnection(TestCase):
    def setUp(self):
        self.connection = telnetconnection.TelnetConnection("localhost")
        self.connection.start = MagicMock()
        self.connection._client = MagicMock()
        self.connection._queue = MagicMock()
        return

    
    def test_procedure_call(self):
        self.connection._client.exec_command.return_value = 1,2,3
        self.connection.iperf("-s", timeout=1)        
        self.connection._client.exec_command.assert_called_with("iperf -s", timeout=1)
        return

    def test_path_argument(self):
        self.connection._client.exec_command.return_value = 0,1,2
        self.connection.ipig("-a all", path="/opt/wifi", timeout=1)
        self.connection._client.exec_command.assert_called_with("/opt/wifi/ipig -a all", timeout=1)
        return
# end class TestLocalConnection
    
