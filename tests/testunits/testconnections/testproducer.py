from unittest import TestCase
from mock import patch, MagicMock

from apetools.connections import producer

class TestPopenProducer(TestCase):
    def setUp(self):
        self.producer = producer.PopenProducer("cmd")
        return

    def test_process(self):
        pipe = MagicMock()
        popen = MagicMock()

        pr = producer.PopenProducer("")
        with patch("subprocess.Popen", popen):
            with patch("subprocess.PIPE", pipe):
                p = pr.process
                c = pr.counter
                self.assertEqual(1, c)
                pr.__del__()
                self.assertEqual(0, c)
        return

    def test_stdout(self):
        pipe = MagicMock()
        popen = MagicMock()

        pr = producer.PopenProducer("")
        with patch("subprocess.Popen", popen):
            with patch("subprocess.PIPE", pipe):
                o = pr.stdout
                c = pr.counter
                self.assertEqual(2, c)
                pr.__del__()
                self.assertEqual(1, c)
                o.__del__()
                self.assertEqual(0, c)
        return

    def test_stdout_stderr(self):
        pipe = MagicMock()
        popen = MagicMock()
        process = MagicMock()
        popen.return_value = process
        
        pr = producer.PopenProducer("")
        process.poll.return_value = None
        with patch("subprocess.Popen", popen):
            with patch("subprocess.PIPE", pipe):
                o = pr.stdout
                e = pr.stderr
                c = pr.counter
                self.assertEqual(3, c)
                pr.__del__()
                self.assertRaises(AssertionError, process.kill.assert_called_once_with)
                self.assertEqual(2, c)
                o.__del__()
                self.assertRaises(AssertionError, process.kill.assert_called_once_with)
                self.assertEqual(1, c)
                e.__del__()
                self.assertEqual(0, c)
                process.kill.assert_called_once_with()
        return

# end class TestPopenProducer
    
