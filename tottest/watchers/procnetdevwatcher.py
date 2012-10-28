"""
A module to watch packets and bytes received on an interface.

This is presumably for monitor-mode wlan interfaces.
"""
import re

from tottest.baseclass import BaseClass
from tottest.parsers import oatbran 


class ProcnetdevWatcherEnum(object):
    """
    A class to hold constants
    """
    __slots__ = ()
    bytes = 'bytes'
    packets = 'packets'
    interface = 'interface'
#end class ProcnetdevWatcherEnum


class ProcnetdevWatcher(BaseClass):
    """
    A class to grab the bytes and packets received at timed intervals.
    """
    def __init__(self, output, interface="wlan0", interval=1):
        """
        :param:

        - `output`: A writeable file-like object
        - `interface`: The name of the interface to watch
        - `interval`: seconds between samples
        """
        super(ProcnetdevWatcher, self).__init__()
        self.output = output
        self.interface = interface
        self.interval = interval
        self._expression = None
        self.stopped = False
        return

    @property
    def expression(self):
        """
        :return: compiled regular expression to match the interface output line
        """
        if self._expression is None:
            interface = oatbran.NAMED(n=ProcnetdevWatcherEnum.interface, e=self.interface) + ":"
            byte_count = oatbran.NAMED(n=ProcnetdevWatcherEnum.bytes, e=oatbran.INTEGER)
            packets = oatbran.NAMED(n=ProcnetdevWatcherEnum.packets, e=oatbran.INTEGER)
            self._expression = re.compile(interface + oatbran.SPACES + byte_count +
                                          oatbran.SPACES + packets)
        return self._expression

    def stop(self):
        """
        :postcondition: `self.stopped` is True
        """
        self.stopped = True
        return
# end class ProcnetdevWatcher
