"""
A module to extract information from `ipconfig`
"""
import re

from tottest.parsers import oatbran

class IpconfigEnum(object):
    __slots__ = ()
    address = "address"


class Ipconfig(object):
    """
    A class to interpret the `ipconfig` output
    """
    def __init__(self, connection, interface="Wireless LAN adapter", not_available="NA"):
        """
        :param:

         - `connection`: a connection to the device
         - `interface`: The name of the interface to check
         - `not_available`: The token to use if the information isn't found
        """
        self.connection = connection
        self.interface = interface
        self.not_available = not_available
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
        for line in output.output:
            if line.startswith(self.interface):
                in_section = True
            elif in_section:
                match = self.ip_expression.search(line)
                if match:
                    return match.groupdict()[IpconfigEnum.address]
        return self.not_available
# end class Ipconfig
