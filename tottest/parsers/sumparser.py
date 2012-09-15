# Copyright (c) 2012 Russell Nakamura

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
The sumparser parses sums and logs the bandwidth sum
"""

from iperfparser import IperfParser 
from iperfexpressions import HumanExpression, ParserKeys, CsvExpression
import oatbran as bran
from coroutine import coroutine

BITS = 'bits'

class HumanExpressionSum(HumanExpression):
    def __init__(self):
        super(HumanExpressionSum, self).__init__()
        return

    @property
    def thread_column(self):
        """
        :return: expression to match the thread (sum) column
        """
        if self._thread_column is None:
            self._thread_column = bran.L_BRACKET + "SUM" + bran.R_BRACKET
        return self._thread_column
# end class HumanExpressionSum

class CsvExpressionSum(CsvExpression):
    def __init__(self):
        super(CsvExpressionSum, self).__init__()
        return

    @property
    def thread_column(self):
        """
        :return: the expression to match the thread (sum) column
        """
        if self._thread_column is None:
            self._thread_column = bran.NAMED(ParserKeys.thread, "-1")
        return self._thread_column

    
class SumParser(IperfParser):
    """
    The SumParser emits bandwidth sum lines
    """
    def __init__(self, *args, **kwargs):
        super(SumParser, self).__init__(*args, **kwargs)
        self.log_format = "({0}) {1} {2}/sec"
        return

    @property
    def regex(self):
        """
        :return: a dictionary of compiled regular expressions
        """
        if self._regex is None:
            self._regex = {ParserKeys.human:HumanExpressionSum().regex,
                           ParserKeys.csv:CsvExpressionSum().regex}
        return self._regex

    def add(self, line):
        """
        :param:

         - `line`: a line of iperf output
        """
        match = self(line)
        if match is not None and self.valid(match):
            bandwidth = self.bandwidth(match)
            self.intervals[float(match[ParserKeys.start])] = bandwidth
            self.logger.info(self.log_format.format(match[ParserKeys.start],
                                                    bandwidth,
                                                    self.units))
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
        while True:
            line = (yield)
            match = self(line)
            if match is not None and self.valid(match):
                # threads is a dict of interval:(thread_count, bandwidths)
                target.send(self.bandwidth(match))
        return
# end class SumParser
