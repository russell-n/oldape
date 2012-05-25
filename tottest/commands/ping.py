"""
A Ping command pings and checks the response.
"""
#python Libraries
import re
from collections import namedtuple

# timetorecovertest Libraries
from timetorecovertest.baseclass import BaseClass
import timetorecovertest.connections.adbconnection as adbconnection

NAMED = r"(?P<{n}>{p})"
ONE_OR_MORE = r"+"
ZERO_OR_MORE = r"*"
DIGIT = r'[0-9]'
SPACE = r'\s'
SPACES = SPACE + ONE_OR_MORE

INTEGER = DIGIT + ONE_OR_MORE
DOT = r"\."
GROUP = "({g})"

REAL = INTEGER + GROUP.format(g= DOT + INTEGER) + ZERO_OR_MORE
M_TO_N_TIMES = "{{{m},{n}}}"

OCTET = DIGIT + M_TO_N_TIMES.format(m=1, n=3)
IP_ADDRESS = NAMED.format(n="ip_address", p=DOT.join([OCTET] * 4))
RTT = NAMED.format(n="rtt", p=REAL)

ADB_PING = SPACES.join([INTEGER, "bytes", "from", IP_ADDRESS + ":",
                        "icmp_seq=" + INTEGER,
                        "ttl=" + INTEGER,
                        "time=" + RTT])

class PingData(namedtuple("PingData", ["target", "rtt"])):
    __slots__ = ()

    def __str__(self):
        return ",".join(["{f}:{v}".format(f=f,v=getattr(self, f)) for f in self._fields])
                   

class ADBPing(BaseClass):
    """
    A ping is a simple ping-command.
    """
    def __init__(self, target=None, *args, **kwargs):
        """
        :param:

         - `target`: An IP Address to ping.
        """
        super(ADBPing, self).__init__(*args, **kwargs)
        self.target = target
        self._connection = None
        self._arguments = None
        self._success_expression = None
        return

    @property
    def connection(self):
        """
        :return: An ADBShellConnection
        """
        if self._connection is None:
            self._connection = adbconnection.ADBShellConnection()
        return self._connection

    @property
    def arguments(self):
        """
        :return: The ping arguments to use
        """
        if self._arguments is None:
            self._arguments = "-c 1 -w 1 {target}".format(target=self.target)
        return self._arguments

    @property
    def success_expression(self):
        """
        :return: compiled regular expressino matching a successful ping.
        """
        if self._success_expression is None:
            self._success_expression = re.compile(ADB_PING)
        return self._success_expression
    
    def run(self, target=None):
        """
        Executes a single ping, checks for a success, returns ping data if it succeeds.

        :param:

         - `target`: The host to ping.
        
        :return: PingData or None
        """
        if target is None:
            target = self.target
        else:
            self._arguments = None
            self.target = target
        for line in self.connection.ping(self.arguments, timeout=1):
            self.logger.debug(line)
            match = self.success_expression.search(line)
            if match:
                return PingData(match.group("ip_address"), match.group('rtt'))
        return
# end class Ping

if __name__ == "__main__":
    ping = ADBPing('192.168.20.1')
    print str(ping.run())
    ping = ADBPing("192.168.30.1")
    print str(ping.run())
