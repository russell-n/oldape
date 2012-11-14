# Copyright 2012 Russell Nakamura
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
A module to watch packets and bytes received on an interface.

This is presumably for monitor-mode wlan interfaces.
"""
import re
from time import time, sleep

from tottest.baseclass import BaseClass
from tottest.parsers import oatbran 
from timestamp import TimestampFormat




class FileExpressionWatcher(BaseClass):
    """
    A class to repeatedly cat a file and output a csv-line
    """
    def __init__(self, output, connection, name, expression, interval=1):
        """
        :param:

        - `output`: A writeable file-like object
        - `interface`: The name of the interface to watch
        - `interval`: seconds between samples
        - `connection`: the connection to the device to watch
        - `name`: the name of the file to watch
        - `expression`: A regular expression with groups to match the output
        """
        super(FileExpressionWatcher, self).__init__()
        self.output = output
        self.interval = interval
        self.connection = connection
        self.expression = expression
        self._timestamp = None
        self.name = name
        self.stopped = False
        return

    @property
    def expression(self):
        """
        :return: compiled regular expression to match the interface output line
        """
        return self._expression

    @expression.setter
    def expression(self, expr):
        """
        :param:

         - `expr`: A string regular expression to match the file output

        :postcondition: self._expr is a compiled regular expression        
        """
        self._expression = re.compile(expr)
        return
    
    @property
    def timestamp(self):
        """
        :return: timestamper 
        """
        if self._timestamp is None:
            self._timestamp = TimestampFormat()
        return self._timestamp
    
    def stop(self):
        """
        :postcondition: `self.stopped` is True
        """
        self.stopped = True
        return

    def __call__(self):
        self.output.write("timestamp,interface,packets,bytes\n")
        start = time()
        output, error = self.connection.cat(self.name)
        for line in output:
            match = self.expression.search(line)
            if match:
                match  = match.groupdict()
                start_bytes = int(match[ProcnetdevWatcherEnum.bytes])
                start_packets = int(match[ProcnetdevWatcherEnum.packets])
            try:
                sleep(self.interval - (time() - start))
            except IOError:
                pass
        while not self.stopped:                
            start = time()
            output, error = self.connection.cat(self.name)
            for line in output:
                match = self.expression.search(line)
                if match:
                    match = match.groupdict()
                    next_bytes = int(match[ProcnetdevWatcherEnum.bytes])
                    next_packets = int(match[ProcnetdevWatcherEnum.packets])
                    self.output.write("{0},{1},{2},{3}\n".format(self.timestamp.now, match[ProcnetdevWatcherEnum.interface],
                                                                 next_packets - start_packets,
                                                                 next_bytes - start_bytes))
                    start_bytes, start_packets = next_bytes, next_packets
            try:
                sleep(self.interval - (time() - start))
            except IOError:
                self.logger.debug("cat {0} took more than one second".format(self.name))

        return
# end class ProcnetdevWatcher

                                  
if __name__ == "__main__":
    from tottest.connections.sshconnection import SSHConnection
    import sys                                  
    c = SSHConnection("portege", "portegeadmin")
    p = ProcnetdevWatcher(sys.stdout, c, "wlan0")
    p()
