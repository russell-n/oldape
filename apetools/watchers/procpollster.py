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
from abc import ABCMeta, abstractproperty

# third-party module
import numpy

#apetools
from apetools.baseclass import BaseClass
from apetools.parsers import oatbran 
from apetools.commons.timestamp import TimestampFormat, TimestampFormatEnums

class BaseProcPolster(BaseClass):
    """
    A base-class for polling proc-files
    """
    __metaclass__ = ABCMeta
    def __init__(self, output, connection, interval=1,
                 name="/proc/net/dev", timestamp_format=TimestampFormatEnums.log,
                 use_header=True):
        """
        :param:

        - `output`: A writeable file-like object
        - `interval`: seconds between samples
        - `connection`: the connection to the device to watch
        - `name`: the name of the file to watch
        - `timestamp_format`: format for timestamps
        - `use_header`: If True, prepend header to output
        """
        super(BaseProcPolster, self).__init__()
        self._logger = None
        self.output = output
        self.interval = interval
        self.connection = connection
        self.timestamp_format = timestamp_format
        self.use_header = use_header
        self._header = None
        self._expression_keys = None
        self._expression = None
        self._timestamp = None
        self.name = name
        self.stopped = False
        return

    @abstractproperty
    def expression(self):
        """
        :return: compiled regular expression to match the outputline
        """
        return self._expression

    @abstractproperty
    def expression_keys(self):
        """
        :return: the keys to the expression groupdict
        """
        return self._expression_keys

    @abstractproperty
    def header(self):
        """
        :return: first line of output file
        """
        return self._header
    
    @property
    def timestamp(self):
        """
        :return: timestamper 
        """
        if self._timestamp is None:
            self._timestamp = TimestampFormat(self.timestamp_format)
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
        if self.use_header:
            self.output.write(self.header)
        start = time()
        output, error = self.connection.cat(self.name)
        start_array = numpy.zeros(len(self.expression_keys), dtype=object)
        next_array = numpy.zeros(len(self.expression_keys), dtype=object)
        #enum = ProcnetdevWatcherEnum
        for line in output:
            match = self.expression.search(line)
            if match:
                self.logger.debug(line)
                match  = match.groupdict()
                for value_index, expression_key in enumerate(self.expression_keys):
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
                    tstamp = self.timestamp.now
                    self.logger.debug(line)
                    match = match.groupdict()
                    for value_index, expression_key  in enumerate(self.expression_keys):
                        next_array[value_index] = int(match[expression_key])
                    
                    self.output.write("{0},{1}\n".format(tstamp,
                                                         ",".join((str(i) for i in (next_array - start_array)))))
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
        name = self.name.replace('/', '')
        self.thread = threading.Thread(target=self.run, name=name)
        self.thread.daemon = True
        self.thread.start()
        return 
# end class BaseProcPollster

class ProcnetdevPollsterEnum(object):
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
#end class ProcnetdevPollsterEnum

class ProcnetdevPollsterIndices(object):
    """
    A class to hold indices to place the values in order
    """
    __slots__ = ()
    rbytes, rpackets, rerrs, rdrop, rfifo, rframe = range(6)
    tbytes, tpackets, terrs, tdrop, tfifo, tcolls, tcarrier = range(6,13)
# end class ProcnetdevPollsterIndices

class ProcnetdevPollster(BaseProcPolster):
    """
    A class to grab the bytes and packets received at timed intervals.
    """
    def __init__(self, interface, *args, **kwargs):
        """
        :param:

        - `output`: A writeable file-like object
        - `interface`: The name of the interface to watch
        - `interval`: seconds between samples
        - `connection`: the connection to the device to watch
        - `name`: the name of the file to watch
        """
        super(ProcnetdevPollster, self).__init__(*args, **kwargs)
        self.interface = interface
        self._rexpression_keys = None
        self._texpression_keys = None
        return

    @property
    def expression_keys(self):
        """
        :return: keys for the regex groupdict
        """
        if self._expression_keys is None:
            # this is explicitly stated to preserve the ordering
            self._expression_keys = ('receive_bytes  receive_packets  receive_errs '
                                     'receive_drop   receive_fifo     receive_frame '
                                     'transmit_bytes transmit_packets transmit_errs '
                                     'transmit_drop  transmit_fifo    transmit_colls '
                                     'transmit_carrier').split()
        return self._expression_keys

    @property
    def rexpression_keys(self):
        """
        :return: subset of keys needed for receiving
        """
        if self._rexpression_keys is None:
            self._rexpression_keys = [v for v in self.expression_keys if v.startswith('r')]
        return self._rexpression_keys

    @property
    def texpression_keys(self):
        """
        :return: subset of keys needed for transmitting
        """
        if self._texpression_keys is None:
            self._texpression_keys = [v for v in self._expression_keys if v.startswith('t')]
        return self._texpression_keys

    @property
    def header(self):
        """
        :return: the first line for the output file
        """
        if self._header is None:
            self._header = ("rbytes,rpackets,rerrs,rdrop,rfifo,tbytes,tpackets,terrs,"
                            "tdrop,tfifo,tcolls,tcarrier\n")
        return self._header
    
    @property
    def expression(self):
        """
        :return: compiled regular expression to match the interface output line
        """
        if self._expression is None:
            integer = oatbran.INTEGER
            enum = ProcnetdevPollsterEnum
            named = oatbran.NAMED
            
            interface = named(n=enum.interface, e=self.interface) + ":"
            rx_values = [named(n=name, e=integer) for name in self.rexpression_keys]
            tx_values = [named(n=name, e=integer) for name in self.texpression_keys]
            self._expression = re.compile(oatbran.SPACES.join([interface] + rx_values + [integer] * 2 + tx_values))
        return self._expression

# end class ProcnetdevPollster

                                  
if __name__ == "__main__":
    from apetools.connections.sshconnection import SSHConnection
    import sys                                  
    c = SSHConnection("portege", "portegeadmin")
    p = ProcnetdevPollster(sys.stdout, c, "wlan0")
    p()
