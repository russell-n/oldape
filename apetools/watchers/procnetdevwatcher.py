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

This was originally for monitor-mode wlan interfaces but is now meant to look for errors
"""
#python standard library
import re
from time import time, sleep
import threading

# third-party module
import numpy

#apetools
from apetools.baseclass import BaseClass
from apetools.parsers import oatbran 
from apetools.commons.timestamp import TimestampFormat


class ProcnetdevWatcherEnum(object):
    """
    A class to hold constants
    """
    __slots__ = ()
    interface = 'interface'
    
    receive_bytes = 'receive_bytes'
    receive_packets = 'receive_packets'
    receive_errs = 'receive_errs'
    receive_drop = 'receive_drop'
    receive_fifo = 'receive_fifo'
    receive_frame = 'receive_frame'
    transmit_bytes = 'transmit_bytes'
    transmit_packets = 'transmit_packets'
    transmit_errs = 'transmit_errs'
    transmit_drop = 'transmit_drop'
    transmit_fifo = 'transmit_fifo'
    transmit_colls = 'transmit_colls'
    transmit_carrier = 'transmit_carrier'
#end class ProcnetdevWatcherEnum

class ProcnetdevWatcherIndices(object):
    """
    A class to hold indices to place the values in order
    """
    __slots__ = ()
    rbytes, rpackets, rerrs, rdrop, rfifo, rframe = range(6)
    tbytes, tpackets, terrs, tdrop, tfifo, tcolls, tcarrier = range(6,13)
# end class ProcnetdevWatcherIndices

HEADER = "rbytes,rpackets,rerrs,rdrop,rfifo,tbytes,tpackets,terrs,tdrop,tfifo,tcolls,tcarrier\n"
EXPRESSION_KEYS = ['receive_bytes', 'receive_packets', 'receive_errs', 'receive_drop', 'receive_fifo',
                   'receive_frame', 'transmit_bytes', 'transmit_packets', 'transmit_errs','transmit_drop',
                   'transmit_fifo', 'transmit_colls', 'transmit_carrier']
REXPRESSION_KEYS = [v for v in EXPRESSION_KEYS if v.startswith('r')]
TEXPRESSION_KEYS = [v for v in EXPRESSION_KEYS if v.startswith('t')]
EXPRESSION_INDICES = zip(EXPRESSION_KEYS, range(13))

class ProcnetdevWatcher(BaseClass):
    """
    A class to grab the bytes and packets received at timed intervals.
    """
    def __init__(self, output, connection, interface, interval=1,
                 name="/proc/net/dev"):
        """
        :param:

        - `output`: A writeable file-like object
        - `interface`: The name of the interface to watch
        - `interval`: seconds between samples
        - `connection`: the connection to the device to watch
        - `name`: the name of the file to watch
        """
        super(ProcnetdevWatcher, self).__init__()
        self.output = output
        self.interface = interface
        self.interval = interval
        self.connection = connection
        self._expression = None
        self._timestamp = None
        self.name = name
        self.stopped = False
        return

    @property
    def expression(self):
        """
        :return: compiled regular expression to match the interface output line
        """
        if self._expression is None:
            integer = oatbran.INTEGER
            enum = ProcnetdevWatcherEnum
            named = oatbran.NAMED
            
            interface = named(n=enum.interface, e=self.interface) + ":"
            rx_values = [named(n=name, e=integer) for name in REXPRESSION_KEYS if name.startswith('r')]
            tx_values = [named(n=name, e=integer) for name in TEXPRESSION_KEYS if name.startswith('t')]
            self._expression = re.compile(oatbran.SPACES.join([interface] + rx_values + [integer] * 2 + tx_values))
        return self._expression

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

    def run(self):
        """
        The main loop
        """
        self.output.write(HEADER)
        start = time()
        output, error = self.connection.cat(self.name)
        start_array = numpy.zeros(len(EXPRESSION_KEYS), dtype=object)
        next_array = numpy.zeros(len(EXPRESSION_KEYS), dtype=object)
        #enum = ProcnetdevWatcherEnum
        for line in output:
            match = self.expression.search(line)
            if match:
                self.logger.debug(line)
                match  = match.groupdict()
                for expression_key, value_index in EXPRESSION_INDICES:
                    start_array[value_index] = int(match[expression_key])
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
                    self.logger.debug(line)
                    match = match.groupdict()
                    for expression_key, value_index in EXPRESSION_INDICES:
                        next_array[value_index] = int(match[expression_key])
                    self.output.write("{0}\n".format(",".join((str(i) for i in (next_array - start_array)))))
                    start_array = numpy.copy(next_array)
            try:
                sleep(self.interval - (time() - start))
            except IOError:
                self.logger.debug("cat {0} took more than one second".format(self.name))

        return

    def start(self):
        """
        :postcondition: run is running in a thread (self.thread)
        """
        self.stopped = False
        self.thread = threading.Thread(target=self.run, name="procnetdevwatcher")
        self.thread.daemon = True
        self.thread.start()
        return 
# end class ProcnetdevWatcher

                                  
if __name__ == "__main__":
    from apetools.connections.sshconnection import SSHConnection
    import sys                                  
    c = SSHConnection("portege", "portegeadmin")
    p = ProcnetdevWatcher(sys.stdout, c, "wlan0")
    p()
