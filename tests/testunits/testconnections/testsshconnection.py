from unittest import TestCase

from mock import MagicMock

from tottest.connections import sshconnection

DEFAULT_PATH = "/sys:/bin"


class TestSSHConnection(TestCase):
    def setUp(self):
        self.connection = sshconnection.SSHConnection("localhost", username="cowman")
        self.connection.start = MagicMock()
        self.connection._client = MagicMock()
        return

    #def test_add_to_path(self):
    #    output = MagicMock()
    #    output.readline.return_value = DEFAULT_PATH
    #
    #    self.connection.queue.get.return_value = (output, None)
    #    paths = "/opt/wifi /mnt/sdcard".split()
    #    self.connection.add_paths(paths)
    #    expected = "PATH={0}:{1};".format(":".join(paths), DEFAULT_PATH)
    #    self.assertEqual(expected, self.connection.command_prefix)
    #    return

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
# end class TestSSHConnection
