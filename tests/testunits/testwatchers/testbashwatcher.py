# python standard library
from unittest import TestCase
from StringIO import StringIO
import time

#third-party
from mock import MagicMock, patch

#tottest
from tottest.watchers.commandwatcher import CommandWatcher

OUTPUT = """
[INFO]  SSID:    allionstaff
[INFO]  BSSID:   18:33:9D:F9:AD:10
[INFO]  IP:      192.168.20.79
[INFO]  RSSI:    -45 dbm
[INFO]  RSSI[0]: -46 dBm
[INFO]  RSSI[1]: -50 dBm
[INFO]  Noise:   -95 dBm
[INFO]  BitRate: 144.4Mb/s
[INFO]  TX pwr:  21 dBm 
"""
timestamp = "20121113152802"
EXPECTED = timestamp +",allionstaff,18:33:9D:F9:AD:10,192.168.20.79,-45,-46,-50,-95,144.4Mb/s,21\n"
BASE = r"\s*[^s]+:\s+([^\s]+)"
EXPRESSION = BASE
              

class TestCommandWatcher(TestCase):
    def setUp(self):
        self.output = MagicMock()
        self.connection = MagicMock()
        self.watcher = CommandWatcher(output=self.output,
                                   connection=self.connection,
                                   command="wifi.sh status",
                                   expression=EXPRESSION)
        return

    def test_expression(self):
        self.connection.sh.return_value = (StringIO(OUTPUT),"")

        now = MagicMock(return_value=timestamp)
        with patch('time.strftime', now):
            self.watcher.start()

            self.watcher.stop()
            time.sleep(1)
        self.connection.sh.assert_called_with("wifi.sh status")
        self.output.write.assert_called_with(EXPECTED)
        return
# end class TestBashWatcher
        
