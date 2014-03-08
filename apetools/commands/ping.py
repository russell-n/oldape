
#python Libraries
import re
from collections import namedtuple

# apetools Libraries
from apetools.baseclass import BaseClass
from apetools.commons import expressions
from apetools.commons.enumerations import OperatingSystem
from apetools.commons import errors

ConfigurationError = errors.ConfigurationError


UNKNOWN_HOST = 'unknown host'
NEWLINE = "\n"


class PingData(namedtuple("PingData", ["target", "rtt"])):
    __slots__ = ()

    def __str__(self):
        return ",".join(["{f}:{v}".format(f=f,v=getattr(self, f)) for f in self._fields])


class PingArguments(object):
    """
    PingArguments is a holder of ping arguments 
    """
    __slots__ = ()
    arguments = {OperatingSystem.android:' -c 1 -w 1 ',
                 OperatingSystem.linux:" -c 1 -w 1 ",
                 OperatingSystem.windows:"-n 1 -w 1000 ",
                 OperatingSystem.mac:' -c 1 -t 1 ',
                 OperatingSystem.ios:' -c 1 '}
# end class PingArguments


class PingCommand(BaseClass):
    """
    A ping is a simple ping-command.
    """
    def __init__(self, target=None, connection=None, operating_system=None):
        """
        PingCommand constructor
        
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
            try:
                self._arguments = PingArguments.arguments[self.operating_system] + self.target
            except KeyError as error:
                self.logger.error(error)
                self.logger.warning('unknown OS ({0}), using Linux'.format(self.operating_system))
                self._arguments = PingArguments.arguments[OperatingSystem.linux] +  self.target
        return self._arguments

    @property
    def expression(self):
        """
        :return: compiled regular expression matching a successful ping.
        """
        if self._expression is None:
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
            self.logger.debug(line.rstrip(NEWLINE))
            match = self.expression.search(line)
            if match:
                return PingData(match.group("ip_address"), match.group('rtt'))
            if UNKNOWN_HOST in line:
                raise ConfigurationError("Unknown Host: {0}".format(target))
        err = error.readline()
        if len(err):
            self.logger.error(err)
        return

    def __call__(self, target, connection):
        """
        Executes a single ping, checks for a success, returns ping data if it succeeds.

        :param:

         - `target`: Address to ping
         - `connection`: the connection to the originator of the ping
        
        :return: PingData or None
        :raise: ConfigurationError if the target is unknown
        """
        self.operating_system = connection.operating_system
        self.target = target
        #import pudb; pudb.set_trace()
        output, error = connection.ping(self.arguments, timeout=5)
        for line in output:
            self.logger.debug(line.rstrip(NEWLINE))
            match = self.expression.search(line)
            if match:
                return PingData(match.group("ip_address"), match.group('rtt'))
            if UNKNOWN_HOST in line:
                raise ConfigurationError("Unknown Host: {0}".format(self.target))
        err = error.readline()
        if len(err):
            self.logger.error(err)
        return
# end class Ping
