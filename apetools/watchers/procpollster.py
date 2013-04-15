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
from time import time, sleep
import threading
from abc import ABCMeta, abstractproperty

# third-party module
import numpy

#apetools
from basepollster import BasePollster
from apetools.parsers import oatbran


class BaseProcPollster(BasePollster):
    """
    A base-class for polling proc-files
    """
    __metaclass__ = ABCMeta
    def __init__(self, *args, **kwargs):
        """
        :param:

        - `output`: A writeable file-like object
        - `interval`: seconds between samples
        - `expression`: a regular expression to match the output
        - `device`: the to the device to watch
        - `name`: the name of the file to watch
        - `timestamp_format`: format for timestamps
        - `use_header`: If True, prepend header to output
        """
        super(BaseProcPollster, self).__init__(*args, **kwargs)
        self._logger = None
        self._header = None
        self._expression_keys = None
        self._connection = None
        self.stopped = False
        return

    @property
    def connection(self):
        """
        :return: the node's connection
        """
        if self._connection is None:
            self._connection = self.device.connection
        return self._connection

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
            match = self.regex.search(line)
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
                match = self.regex.search(line)
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
        self.thread = threading.Thread(target=self.run_thread, name=name)
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

class ProcnetdevPollster(BaseProcPollster):
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
    def name(self):
        """
        :return: the name for logging (or the name of the file)
        """
        if self._name is None:
            self._name = "/proc/net/dev"
        return self._name


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
            self._header = ("timestamp,rx_bytes,rx_packets,rx_errs,rx_drop,rx_fifo,rx_frame,tx_bytes,"
                            "tx_packets,tx_errs,"
                            "txdrop,tx_fifo,tx_colls,tx_carrier\n")
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
            self._expression = oatbran.SPACES.join([interface] + rx_values + [integer] * 2 + tx_values)
        return self._expression

# end class ProcnetdevPollster


class CpuPollsterEnum(object):
    __slots = ()
    user = 'user'
    nice = 'nice'
    system = 'system'
    idle = 'idle'
    # end class CpuPollsterEnum

class CpuPollster(BaseProcPollster):
    """
    A class to grab the percent of CPU used.
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

        - `output`: A writeable file-like object
        - `interface`: The name of the interface to watch
        - `interval`: seconds between samples
        - `connection`: the connection to the device to watch
        - `name`: the name of the file to watch
        """
        super(CpuPollster, self).__init__(*args, **kwargs)
        return

    @property
    def name(self):
        """
        :return: the name for logging (or the name of the file)
        """
        if self._name is None:
            self._name = "/proc/stat"
        return self._name


    @property
    def expression_keys(self):
        """
        :return: keys for the regex groupdict
        """
        if self._expression_keys is None:
            # this is explicitly stated to preserve the ordering
            self._expression_keys = (CpuPollsterEnum.user,
                                     CpuPollsterEnum.nice,
                                     CpuPollsterEnum.system,
                                     CpuPollsterEnum.idle)
        return self._expression_keys

    @property
    def header(self):
        """
        :return: the first line for the output file
        """
        if self._header is None:
            self._header = "timestamp,cpu_percent\n"
        return self._header

    @property
    def expression(self):
        """
        :return: compiled regular expression to match the interface output line
        """
        if self._expression is None:
            integer = oatbran.INTEGER
            enum = CpuPollsterEnum
            named = oatbran.NAMED
            spaces = oatbran.SPACES

            user = named(n=enum.user, e=integer)
            nice = named(n=enum.nice, e=integer)
            system = named(n=enum.system, e=integer)
            idle = named(n=enum.idle, e=integer)
            self._expression = spaces.join(['cpu',
                                            user,
                                            nice,
                                            system,
                                            idle])
        return self._expression

    def run(self):
        """
        The main loop
        """
        self.output.write(self.header)
        start = time()
        lock = self.connection.lock

        with lock:
            output, error = self.connection.cat(self.name)
        start_used = 0
        next_used = 0
        start_total = 0
        next_total = 0

        # get the first sample
        for line in output:
            match = self.regex.search(line)
            if match:
                self.logger.debug(line)
                match  = match.groupdict()

                start_total = sum([int(value) for value in match.itervalues()])
                start_used = start_total - int(match[CpuPollsterEnum.idle])

            try:
                sleep(self.interval - (time() - start))
            except IOError:
                pass

            # watch the file
        while not self.stopped:
            start = time()
            with lock:
                output, error = self.connection.cat(self.name)
            for line in output:
                match = self.regex.search(line)
                if match:
                    tstamp = self.timestamp.now
                    self.logger.debug(line)
                    match = match.groupdict()
                    next_total = sum([int(value) for value in match.itervalues()])
                    next_used = next_total - float(match[CpuPollsterEnum.idle])
                    used = (next_used - start_used)/(next_total - start_total)
                    self.output.write("{0},{1}\n".format(tstamp,
                                                         100 * used))
                    start_used, start_total = next_used, next_total
                    next_used = next_total = 0
                    break
            try:
                sleep(self.interval - (time() - start))
            except IOError:
                self.logger.debug("cat {0} took more than one second".format(self.name))
        return
# end class CpuPollster

if __name__ == "__main__":
    from apetools.connections.sshconnection import SSHConnection
    import sys
    c = SSHConnection("portege", "portegeadmin")
    p = ProcnetdevPollster(sys.stdout, c, "wlan0")
    p()
