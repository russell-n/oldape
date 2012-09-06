"""
The sumparser parses sums and logs the bandwidth sum
"""

from iperfparser import IperfParser 
from iperfexpressions import HumanExpression, ParserKeys, CsvExpression
import oatbran as bran

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

    def __call__(self, line):
        """
        :param:

         - `line`: a line of iperf output
        """
        match = self.match(line)
        if match is not None and self.valid(match):
            bandwidth = self.bandwidth(match)
            self.logger.info(self.log_format.format(match[ParserKeys.start],
                                                    bandwidth,
                                                    self.units))
        else:
            self.logger.debug(line)
        return

    def add(self, line):
        """
        An alias for __call__ to maintain backwards compatability
        """
        self(line)
        return
# end class SumParser
