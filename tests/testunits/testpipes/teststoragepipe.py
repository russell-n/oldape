from unittest import TestCase

from mock import MagicMock, patch

from tottest.pipes.storagepipe import StoragePipe

EOF = ""


class TestStoragePipe(TestCase):
    def setUp(self):
        self.open_file = MagicMock(spec=file)
        self.target = MagicMock()
        self.pipe = StoragePipe(path="here", target=self.target)
        return

    def test_start(self):
        self.pipe.header_token = "cow"
        open_pipe = MagicMock()
        open_file = MagicMock()
        self.open_file.return_value = open_file
        self.target.open.return_value = open_pipe

        os_mock = MagicMock()
        with patch("__builtin__.open", self.open_file, create=True):
            with patch("os.fsync", os_mock):
                output = self.pipe.open_start("test_name")
                self.open_file.assert_called_with("here/test_name", "w")
                self.assertIsNotNone(self.pipe.header_token)
                print self.target.mock_calls
                open_pipe.send.assert_called_with("cow")

                output.send("pie")
                open_file.write.assert_called_with("pie\n")
                open_pipe.send.assert_called_with("pie")

                open_file.close.return_value = MagicMock()
                try:
                    output.send(EOF)
                except StopIteration:
                    pass
                open_file.write.assert_called_with("\n")
                open_pipe.send.assert_called_with(EOF)
                
                open_file.close.assert_called_with()

        return

    def test_pipe(self):
        self.pipe.header_token = "cow"
        open_pipe = MagicMock()
        open_file = MagicMock()
        self.open_file.return_value = open_file
        self.target.open.return_value = open_pipe

        os_mock = MagicMock()
        with patch("__builtin__.open", self.open_file, create=True):
            with patch("os.fsync", os_mock):
                output = self.pipe.open("test_name")
                output.send("boy")
                self.open_file.assert_called_with("here/test_name", "w")

                open_pipe.send.assert_called_with("boy,cow")

                output.send("pie")
                open_file.write.assert_called_with("pie")
                open_pipe.send.assert_called_with("pie")

                open_file.close.return_value = MagicMock()
                try:
                    output.send(EOF)
                except StopIteration:
                    pass
                open_file.write.assert_called_with(EOF)
                open_pipe.send.assert_called_with(EOF)
                
                open_file.close.assert_called_with()
        return

    def test_pipe_sink(self):
        self.pipe.header_token = "cow"
        open_file = MagicMock()
        self.open_file.return_value = open_file

        os_mock = MagicMock()
        with patch("__builtin__.open", self.open_file, create=True):
            with patch("os.fsync", os_mock):
                output = self.pipe.open_sink("test_name")
                output.send("boy")
                self.open_file.assert_called_with("here/test_name", "w")

                output.send("pie")
                open_file.write.assert_called_with("pie\n")

                open_file.close.return_value = MagicMock()
                try:
                    output.send(EOF)
                except StopIteration:
                    pass
                open_file.write.assert_called_with("\n")
                open_file.close.assert_called_with()

        
# end class TestStoragePipe
