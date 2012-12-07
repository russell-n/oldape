from unittest import TestCase
from StringIO import StringIO
import socket
from mock import MagicMock

from apetools.connections.sshconnection import OutputFile

output = """Now is the winter of our discontent,
Made glorious summey by this Son of York,
And all the clouds that lour'd upon this house,
In the deep bosom of the ocean buried."""

NEWLINE = "\n"
EOF = ""

class TestOutputFile(TestCase):
    def setUp(self):
        self.timeout_source = MagicMock()
        self.timeout_source.readline.side_effect = socket.timeout
        self.source = StringIO(output)
        self.output = OutputFile(self.source)
        return

    def test_iter(self):
        lines = output.split(NEWLINE)
        for index, line in enumerate(self.output):
            if line != EOF:
                self.assertEqual(lines[index],line.rstrip(NEWLINE))            
        return

    def test_iter_socket_timeout(self):
        self.output.source = self.timeout_source
        for line in self.output:
            self.assertEqual(EOF, line)
        return

    def test_readline_socket_timeout(self):
        self.output.source = MagicMock()
        self.output.source.readline.side_effect = socket.timeout()
        self.output.source.__iter__ = self.source
        self.output.readline()
        return

    def test_readline(self):
        line = self.output.readline()
        self.assertEqual("Now is the winter of our discontent,",line.rstrip(NEWLINE))
        return

    def test_readlines(self):
        lines = output.split(NEWLINE)
        for index, line in enumerate(self.output.readlines()):
            if line != EOF:
                self.assertEqual(lines[index],line.rstrip(NEWLINE))            
        return

    def test_read(self):
        lines = self.output.read()
        self.assertEqual(output, lines)
        return
# end class TestOutputFile
