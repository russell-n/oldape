"""
A module to build time-to-recovery tools
"""

from tottest.commands import ping
from tottest.tools import timetorecovery

class TimeToRecoveryBuilder(object):
    """
    A builder of TTR Objects
    """
    def __init__(self, target, connection, operating_system=None, timeout=500,
                 threshold=5):
        """
        :param:

         - `target`: The IP address or hostname to ping
         - `connection`: A connection to the device that pings
         - `operating_system`: The operating system of the device that pings
         - `timeout`: The number of seconds to try and ping
         - `threshold`: The number of consecutive pings to qualify as 'success'
        """
        self.target = target
        self.connection = connection
        self.operating_system = operating_system
        self.timeout = timeout
        self.threshold = threshold
        self._pinger = None
        self._ttr = None
        return

    @property
    def pinger(self):
        """
        :return: A Ping Command
        """
        if self._pinger is None:
            self._pinger = ping.PingCommand(target=self.target,
                                            connection=self.connection,                                            
                                            operating_system=self.operating_system)
        return self._pinger

    @property
    def ttr(self):
        """
        :return: A time to recovery object
        """
        if self._ttr is None:
            self._ttr = timetorecovery.TimeToRecovery(pinger=self.pinger,
                                                      target=self.target,
                                                      timeout=self.timeout,
                                                      threshold=self.threshold)
        return self._ttr
# end TimeToRecoveryBuilder
