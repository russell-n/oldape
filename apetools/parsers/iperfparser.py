# Copyright (c) 2012 Russell Nakamura

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# python libraries
from collections import defaultdict, namedtuple
import os

#apetools modules
from apetools.baseclass import BaseClass

from iperfexpressions import HumanExpression, ParserKeys
from iperfexpressions import CsvExpression
from unitconverter import UnitConverter
from coroutine import coroutine

class BandwidthData(namedtuple("BandwidthData", "interval bandwidth units".split())):
    """
    A tuple to hold the bandwidth data
    """
    __slots__ = ()

    def __str__(self):
        return  "{0},{1},{2}/sec".format(self.interval, self.bandwidth, self.units)
# end class BandwidthData
                        
class IperfParser(BaseClass):
    """
    The Iperf Parser extracts bandwidth and other information from the output
    """
    def __init__(self, expected_interval=1, interval_tolerance=0.1, units="Mbits", threads=4):
        """
        :param:

         - `expected_interval`: the seconds between sample reports
         - `interval_tolerance`: upper bound of difference between actual and expected
         - `units`: desired output units (must match iperf output case - e.g. MBytes)
         - `threads`: (number of threads) needed for coroutine and pipe
        """
        super(IperfParser, self).__init__()
        self._logger = None
        self.expected_interval = expected_interval
        self.interval_tolerance = interval_tolerance
        self.units = units
        self.threads = threads
        self._regex = None
        self._human_regex = None
        self._csv_regex = None
        self._combined_regex = None
        self._conversion = None
        self._intervals = None
        self._threads = None
        self.format = None
        self._bandwidths = None

        self.thread_count = 0
        self.current_thread = None
        return

    @property
    def bandwidths(self):
        """
        :return: iterator over the bandwidths
        """
        intervals = sorted(self.intervals.keys())
        for interval in intervals:
            yield self.intervals[interval]
            

    @property
    def regex(self):
        """
        :return: format:regex dictionary
        """
        if self._regex is None:
            self._regex = {ParserKeys.human:HumanExpression().regex,
                           ParserKeys.csv:CsvExpression().regex}
        return self._regex
    
    @property
    def intervals(self):
        """
        :rtype: dict with default values of 0
        :return: interval: bandwidth  
        """
        if self._intervals is None:
            self._intervals = defaultdict(lambda:0)
        return self._intervals

    @property
    def conversion(self):
        """
        :return: UnitConveter nested dictionary
        """
        if self._conversion is None:
            self._conversion = UnitConverter()
        return self._conversion
    
    def valid(self, match):
        """
        :param:

         - `match`: a groupdict containing parsed iperf fields

        :return: True if the end-start interval is valid (within tolerance)
        """
        start, end = float(match[ParserKeys.start]), float(match[ParserKeys.end])
        return (end - start) - self.expected_interval < self.interval_tolerance

    def bandwidth(self, match):
        """
        :param:

         - `match`: A parsed match group dictionary

        :rtype: float
        :return: the bandwidth in the self.units
        """
        bandwidth = float(match[ParserKeys.bandwidth])
        try:
            units = match[ParserKeys.units]
        except KeyError:
            # assume a csv-format
            units = 'bits'
        return self.conversion[units][self.units] * bandwidth

    def __call__(self, line):
        """
        :param:

         - `line`: a line of iperf output

        :return: bandwidth or None
        """
        match = self.search(line)
        bandwidth = None
        if match is not None and self.valid(match):
            self.thread_count = (self.thread_count + 1) % self.threads
            if self.thread_count == 0:
                self.current_thread = float(match[ParserKeys.start])
                bandwidth = self.bandwidth(match)
            self.intervals[float(match[ParserKeys.start])] += self.bandwidth(match)
        return bandwidth
    
    def search(self, line):
        """
        :param:

         - `line`: a string of iperf output
        :return: match dict or None
        """
        try:
            return self.regex[self.format].search(line).groupdict()
        except KeyError:
            self.logger.debug("{0} skipped, format not set".format(line))
        except AttributeError:
            pass

        try:
            match = self.regex[ParserKeys.human].search(line).groupdict()
            self.logger.debug("Matched: {0}".format(line))            
            self.format = ParserKeys.human
            self.logger.debug("Setting format to {0}".format(self.format))
            return match
        except AttributeError:
            pass

        try:
            match = self.regex[ParserKeys.csv].search(line).groupdict()
            self.logger.debug("Matched: {0}".format(line))
            self.format = ParserKeys.csv
            self.logger.debug("Setting format to {0}".format(self.format))
            return match
        except AttributeError:
            pass
        return

    @coroutine
    def pipe(self, target):
        """
        
        :warnings:

         - For bad connections with threads this might break (as the threads die)
         - Use for good connections or live data only (use `bandwidths` and completed data for greater fidelity)
         
        :parameters:

         - `target`: a target to send matched output to

        :send:

         - bandwidth converted to self.units as a float
        """
        threads = defaultdict(lambda:[0,0])
        thread_count = 0
        bandwidth = 1
        while True:
            line = (yield)
            match = self.search(line)
            if match is not None and self.valid(match):
                # threads is a dict of interval:(thread_count, bandwidths)
                interval = match[ParserKeys.start]
                threads[interval][thread_count] += 1
                threads[interval][bandwidth] += self.bandwidth(match)
                for key in threads:
                    if key == min(threads) and threads[interval][thread_count]==self.threads:
                        target.send(threads[interval][bandwidth])
        return
    
    def reset(self):
        """
        Resets the attributes set during parsing
        """
        self.logger.debug("Resetting the IperfParser")
        self.format = None
        self._interval_threads = None
        self._thread_count = None
        self._threads = None
        return

    def filename(self, basename):
        """
        :param:

         - `basename`: a the raw-iperf filename (without path)

        :return: the filename with the extension changed to .csv
        """
        base, ext = os.path.splitext(basename)
        return "{0}.csv".format(base)
# end class IperfParser
