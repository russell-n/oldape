"""
A module to hold a network tester.
"""

#python libraries
import sys

# tottest libraries
from tottest.baseclass import BaseClass
from tottest.commons import errors

NEWLINE = '\n'
ADD_NEWLINE = "{0}" + NEWLINE
COMMA = ","
ADD_COMMA = "{0}" + COMMA


class NetworkTester(BaseClass):
    """
    A network tester runs a series of network tests.
    """
    def __init__(self, testers, output=None):
        """
        :param:

         - `testers`: An iterable set of testers to run
         - `output`: An output to write data to.
        """
        super(NetworkTester, self).__init__()
        self.testers=testers
        self._output = output
        return

    @property
    def output(self):
        """
        :return: The output to write data to.
        """
        if self._output is None:
            self._output = sys.stdout
        return self._output
    
    def run(self):
        """
        Runs the testers

        :raise: ConnectionError if any tester fails.
        """
        failures = []
        for tester in self.testers:
            datum = tester.run()
            if datum is not None:
                self.output.write(ADD_NEWLINE.format(datum))
            else:
                failures.append(tester)
        if len(failures):
            failure_message = "Failed Connections: " + COMMA.join(str(failures))
            self.logger.error(failure_message)
            raise errors.ConnectionError(failure_message)
        return
# end class NetworkTester
    
