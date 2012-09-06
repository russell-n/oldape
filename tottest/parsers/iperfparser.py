"""
The IperfParser parses 
"""
# python libraries
from collections import defaultdict

from tottest.baseclass import BaseClass

from iperfexpressions import HumanExpression, ParserKeys
from iperfexpressions import CsvExpression
from unitconverter import UnitConverter


class IperfParser(BaseClass):
    """
    The Iperf Parser extracts bandwidth and other information from the output
    """
    def __init__(self, expected_interval=1, interval_tolerance=0.1, units="Mbits"):
        """
        :param:

         - `expected_interval`: the seconds between sample reports
         - `interval_tolerance`: upper bound of difference between actual and expected
         - `units`: desired output units (must match iperf output case - e.g. MBytes)
        """
        super(IperfParser, self).__init__()
        self._logger = None
        self.expected_interval = expected_interval
        self.interval_tolerance = interval_tolerance
        self.units = units
        self._regex = None
        self._human_regex = None
        self._csv_regex = None
        self._combined_regex = None
        self._conversion = None
        self._intervals = None
        self.format = None
        self._bandwidths = None
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

        :postcondition: if line matches, the bandwidth is added to intervals
        """
        self.logger.debug("Checking: {0}".format(line))
        match = self.match(line)
        if match is not None and self.valid(match):
            self.logger.debug("Setting interval")
            self.intervals[float(match[ParserKeys.start])] += self.bandwidth(match)
        return

    def add(self, line):
        """
        An alias for __call__ to remain backwards-compatible.
        """
        self(line)
        return
    
    def match(self, line):
        """
        :param:

         - `line`: a string of iperf output

        :return: match dict or None
        """
        try:
            return self.regex[self.format].search(line).groupdict()
        except KeyError:
            self.logger.debug("'{0}' passed on, format not set".format(line))
        except AttributeError:
            pass

        try:
            match = self.regex[ParserKeys.human].search(line).groupdict()
            self.format = ParserKeys.human
            self.logger.debug("Setting format to {0}".format(self.format))
            return match
        except AttributeError:
            pass

        try:
            match = self.regex[ParserKeys.csv].search(line).groupdict()
            self.format = ParserKeys.csv
            self.logger.debug("Setting format to {0}".format(self.format))
            return match
        except AttributeError:
            pass
        return

    def reset(self):
        """
        Resets the attributes set during parsing
        """
        self.format = None
        self._interval_threads = None
        return
# end class IperfParser
