"""
A module to watch frame and byte-counts using tshark
"""
import sys
import re
import time

from tottest.parsers import oatbran
from tottest.baseclass import BaseClass
from timestamp import TimestampFormat

class TsharkWatcherEnum(object):
    """
    A class to hold variable names 
    """
    __slots__ = ()
    frames = "frames"
    bytes = 'bytes'
    
# end class TsharkWatcherEnum

    
class TsharkWatcher(BaseClass):
    """
    A class to watch bytes and frames using tshark
    """
    def __init__(self, connection, output=None, interface="wlan0"):
        """
        :param:

         - `output`: file to send output to 
         -`connection`: connection to the device to run tshark
         - `interface`: network interface to monitor
        """
        super(TsharkWatcher, self).__init__()
        self._output = output
        self.connection = connection
        self._expression = None
        self.frames = None
        self._timestamp = None
        self.stopped = False
        self.interface = interface
        return

    @property
    def timestamp(self):
        """
        :return: timestamper
        """
        if self._timestamp is None:
            self._timestamp = TimestampFormat()
        return self._timestamp

    @property
    def output(self):
        """
        :return: file object to write to
        """
        if self._output is None:
            self._output = sys.stdout
        return self._output

    @property
    def expression(self):
        """
        :return: a regular expression to match tshark output
        """
        if self._expression is None:
            timestamp = oatbran.REAL + '-'+ oatbran.REAL
            frames = oatbran.NAMED(n=TsharkWatcherEnum.frames, e=oatbran.INTEGER)
            byte = oatbran.NAMED(n=TsharkWatcherEnum.bytes, e=oatbran.INTEGER)
            self._expression = re.compile(timestamp + oatbran.SPACES
                                          + frames+ oatbran.SPACES
                                          + byte)
        return self._expression

    def call_once(self):
        """
        :return: timestamp, frames, bytes
        """
        timestamp = self.timestamp.now
        byte_count = 0
        frames = 0
        output, error = self.connection.tshark("-i {0} -nqz io,stat,1 -a duration:1".format(self.interface))
        for line in output:
            match = self.expression.search(line)
            if match:
                match = match.groupdict()
                frames += int(match[TsharkWatcherEnum.frames])
                byte_count += int(match[TsharkWatcherEnum.bytes])                
        return timestamp, frames, byte_count

    def stop(self):
        """
        :postcondition: self.stopped is True
        """
        self.stopped = True
        return
    
    def __call__(self):
        """
        :postcondition: tshark data sent to self.output
        """
        self.output.write("timestamp,frames,bytes\n")
        start_time = time.time()
        while not self.stopped:
            time_stamp, next_frames, next_bytes = self.call_once()
            self.output.write("{0},{1},{2}\n".format(time_stamp,
                                                     next_frames,
                                                     next_bytes))

            try:
                time.sleep(1 - (time.time() - start_time))
            except IOError:
                self.logger.debug("tshark took more than 1 second")

        return
# end class TsharkWatcher

if __name__ == "__main__":
    from tottest.connections.sshconnection import SSHConnection
    c = SSHConnection("portege", "portegeadmin")
    watch = TsharkWatcher(c)
    watch()
