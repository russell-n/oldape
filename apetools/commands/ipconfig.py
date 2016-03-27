
# python
import re
from time import time as now

#apetools
from apetools.parsers import oatbran
from apetools.baseclass import BaseClass
from apetools.commons.errors import CommandError

NEWLINE = "\n"

class IpconfigEnum(object):
    __slots__ = ()
    address = "address"
# end class IpConfigEnum

class IpconfigError(CommandError):
    """
    An exception to raise if the command fails.
    """
# end class IpconfigError

class Ipconfig(BaseClass):
    """
    A class to interpret the `ipconfig` output
    """
    def __init__(self, connection, interface="Wireless LAN adapter", not_available="NA",
                 timeout=30):
        """
        :param:

         - `connection`: a connection to the device
         - `interface`: The name of the interface to check
         - `not_available`: The token to use if the information isn't found
         - `timeout`: The amount of time to wait for the command before giving up.
        """
        super(Ipconfig, self).__init__()
        self.connection = connection
        self.interface = interface
        self.not_available = not_available
        self.timeout = timeout
        self._ip_expression = None
        self._address = None
        return

    @property
    def ip_expression(self):
        """
        :return: comiled regular expression to extract the IP address
        """
        if self._ip_expression is None:
            self._ip_expression = re.compile(oatbran.SPACES + "IPv4" + oatbran.SPACES + "Address" + "[\s.]"+
                                             oatbran.ONE_OR_MORE + ":" + oatbran.SPACES+
                                             oatbran.NAMED(n=IpconfigEnum.address,
                                                           e=oatbran.IP_ADDRESS))
        return self._ip_expression

    @property
    def address(self):
        """
        :return: the address of the interface
        """
        output =  self.connection.ipconfig()
        in_section = False

        max_time = now() + self.timeout
        self.logger.debug("Command will timeout in {0} seconds".format(self.timeout))
        for line in output.output:
            self.logger.debug(line.rstrip(NEWLINE))
            if line.startswith(self.interface):
                in_section = True
            elif in_section:
                match = self.ip_expression.search(line)
                if match:
                    return match.groupdict()[IpconfigEnum.address]
            if now() > max_time:
                raise IpconfigError("Command Timed out after {0} seconds.".format(self.timeout))
        return self.not_available
# end class Ipconfig