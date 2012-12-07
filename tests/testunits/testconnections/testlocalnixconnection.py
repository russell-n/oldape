from unittest import TestCase

from mock import MagicMock

from apetools.connections import localconnection

DEFAULT_PATH = "/sys:/bin"


class TestLocalNixConnection(TestCase):
    def setUp(self):
        self.connection = localconnection.LocalNixConnection()
        self.connection.start = MagicMock()
        self.connection._queue = MagicMock()
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
