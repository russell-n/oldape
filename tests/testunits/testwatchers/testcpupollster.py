#python standard library
from unittest import TestCase
import time

# third-party
from mock import MagicMock, call, patch, PropertyMock

# apetools
from apetools.watchers.procpollster import CpuPollster

total_1 = 5490222 + 307769 + 8850323 + 597307292
used_1 =  5490222 + 307769 + 8850323 
sample_1 = """
cpu  5490222 307769 8850323 597307292 855706 7 494759 0 0 0
cpu0 5490222 307769 8850323 597307292 855706 7 494759 0 0 0
intr 619304578 0 188353388 0 0 0 2 2 2 2 0 0 86440905 0 0 0 0 0 0 0 69744968 0 0 0 0 0 0 0 0 274764932 0 0 0 0 352 0 0 0 0 0 0 0 0 0 0 0 0 25 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
ctxt 968642713
btime 1353981250
processes 5981957
procs_running 1
procs_blocked 0
softirq 605048043 0 160578097 3066595 247404048 2210292 0 352 0 15530 191773129
""".split('\n')

total_2 = 5490222 + 307769 + 8850324 + 597309744
used_2 =  5490222 + 307769 + 8850324 

sample_2 = """
cpu  5490222 307769 8850324 597309744 855706 7 494759 0 0 0
cpu0 5490222 307769 8850324 597309744 855706 7 494759 0 0 0
intr 619306319 0 188353965 0 0 0 2 2 2 2 0 0 86440977 0 0 0 0 0 0 0 69744968 0 0 0 0 0 0 0 0 274766024 0 0 0 0 352 0 0 0 0 0 0 0 0 0 0 0 0 25 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
ctxt 968645023
btime 1353981250
processes 5981959
procs_running 1
procs_blocked 0
softirq 605049116 0 160578591 3066608 247404120 2210292 0 352 0 15530 191773623
""".split('\n')

TIMESTAMP = 'now'

class CpuPollsterTest(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.device = MagicMock()
        self.device.connection =self.connection
        self.output = MagicMock()
        self.timestamp = MagicMock() 
        self.watcher = CpuPollster(output=self.output,
                                    device=self.device)
        self.watcher._timestamp = self.timestamp
        return

    def test_call(self):
        output = [(sample_1, ''), (sample_2, '')]
        def side_effects(*args, **kwargs):
            return output.pop(0)
        self.connection.cat.side_effect = side_effects
        timer = MagicMock()
        expected = [call.write(self.watcher.header), 
                    call.write("{0}\n".format(100 * (used_2 - used_1)/(total_2 - total_1)))]
        self.timestamp.now.return_value = TIMESTAMP
        timer.return_value = 0
        self.assertTrue(self.watcher.use_header)
        with patch('time.time', timer):
            with patch('apetools.commons.timestamp.TimestampFormat.now', new_callable=PropertyMock) as mock_now:
                mock_now.__get__ = MagicMock(return_value = TIMESTAMP)
                self.watcher._timestamp = None
                self.watcher.start()
                time.sleep(1)
                self.watcher.stop()
        calls = self.output.write.call_args_list
        self.assertEqual(expected, calls)

        return
# end class CpuPollsterTest
