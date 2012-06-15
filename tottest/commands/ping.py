"""
A Ping command pings and checks the response.
"""
#python Libraries
import re
from collections import namedtuple

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.commons import expressions
from tottest.commons import enumerations
from tottest.commons import errors

ConfigurationError = errors.ConfigurationError

UNKNOWN_HOST = 'unknown host'

class PingData(namedtuple("PingData", ["target", "rtt"])):
    __slots__ = ()

    def __str__(self):
        return ",".join(["{f}:{v}".format(f=f,v=getattr(self, f)) for f in self._fields])
                   

class PingArguments(object):
    """
    PingArguments is a holder of ping arguments
    """
    android = ' -c 1 -w 1 '

    
    
class PingCommand(BaseClass):
    """
    A ping is a simple ping-command.
    """
    def __init__(self, target, connection, operating_system):
        """
        :param:

         - `target`: An IP Address to ping.
         - `connection`: A Connection to the device
         - `operating_system`: The operating system of the device
        """
        super(PingCommand, self).__init__()
        self.target = target
        self.connection = connection
        self.operating_system = operating_system
        self._arguments = None
        self._expression = None
        return

    @property
    def arguments(self):
        """
        :return: The ping arguments to use
        """
        if self._arguments is None:
            if self.operating_system == enumerations.OperatingSystem.android:
                self._arguments = "-c 1 -w 1 {target}".format(target=self.target)
        return self._arguments

    @property
    def expression(self):
        """
        :return: compiled regular expression matching a successful ping.
        """
        if self._expression is None:
            if self.operating_system in (enumerations.OperatingSystem.android,
                                         enumerations.OperatingSystem.linux):
                expression = expressions.PING
            self._expression = re.compile(expression)
        return self._expression
    
    def run(self, target=None):
        """
        Executes a single ping, checks for a success, returns ping data if it succeeds.

        :param:

         - `target`: The host to ping.
        
        :return: PingData or None
        :raise: ConfigurationError if the target is unknown
        """
        if target is None:
            target = self.target
        else:
            self._arguments = None
            self.target = target
        output, error = self.connection.ping(self.arguments, timeout=1)
        for line in output:
            self.logger.debug(line)
            match = self.expression.search(line)
            if match:
                return PingData(match.group("ip_address"), match.group('rtt'))
            if UNKNOWN_HOST in line:
                raise ConfigurationError("Unknown Host: {0}".format(target))
        return
# end class Ping

if __name__ == "__main__":
    ping = PingCommand('192.168.20.1')
    print str(ping.run())
    ping = PingCommand("192.168.30.1")
    print str(ping.run())
