"""
A command to interpret the output of Miller's rssi puller
"""
import re

from tottest.parsers import oatbran
from tottest.commons.errors import CommandError
from tottest.baseclass import BaseClass

class WinRssiError(CommandError):
    """
    A Win Rssi Error is raised if the output of Miller's rssi indicates a known error
    """
# end WinRssiError

NA = "NA"

class WinRssi(BaseClass):
    """
    A class to get the rssi via an installed version of miller's rssi puller.
    """
    def __init__(self, connection):
        """
        :param:

         - `connection`: a connection to the windows device
        """
        super(WinRssi, self).__init__()
        self.connection = connection
        self._expression = None
        self.key = "rssi"
        return

    @property
    def expression(self):
        """
        :return: compiled regular expression to match valid rssi output
        """
        if self._expression is None:
            self._expression = re.compile(oatbran.NAMED(n=self.key, e="-" + oatbran.INTEGER))
        return self._expression

    def validate(self, line):
        """
        :parameter:

         - `line`: a line of output
        """
        self.logger.debug("Validating: {0}".format(line))
        if "Unable to find the wireless interface." in line:
            raise WinRssiError(line)
        if "The group or resource is not in the correct state" in line:
            raise WinRssiError(line)
        return

    def __call__(self):
        """
        :return: the rssi value
        :raises: CommandError if the rssi can't be retrieved.
        """
        output = self.connection.rssi()
        for line in output.output:
            match = self.expression.search(line)
            if match:
                self.logger.debug("Matched: {0}".format(line))
                return match.groupdict()[self.key]
            self.validate(line)
        return NA
# end class WinRssi
