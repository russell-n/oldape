"""
The time to failure pings a target until the pings fail.
"""
#python
import time
now = time.time

from collections import namedtuple

# tottest libraries
from tottest.baseclass import BaseClass

from tottest.commands import ping

TTRData = namedtuple("TTRData", "ttr rtt")


class TimeToRecovery(BaseClass):
    """
    A TimeToRecovery pings a target until the pings succeeed.
    """
    def __init__(self, pinger=None, target=None, timeout=300,
                 threshold=5):
        """
        :param:

         - `pinger`: An object to ping a target.
         - `target`: The target address to ping
         - `timeout`: The length of time to try in seconds.
         - `threshold`: The number of consecutive pings to make a recovery
        """
        super(TimeToRecovery, self).__init__()
        self._pinger = pinger
        self.target = target
        self.target = target
        self.timeout = timeout
        self.threshold = threshold
        return

    @property
    def pinger(self):
        """
        :return: A pinger object
        """
        if self._pinger is None:
            self._pinger = ping.ADBPing()
        return self._pinger

    def _unpack_parameters(self, parameters):
        if parameters is None:
            return self.target, self.timeout, self.threshold
        else:
            return parameters.target, parameters.timeout, parameters.threshold
        
    def run(self, parameters=None):
        """
        Pings until failure or timeout.

        :param:

         - `parameters.target`: The address to ping.
         - `parameters.timeout`: The length of time to try (in seconds)
         - `parameters.threshold`: The number of consecutive pings needed to be a success.

        :rtype: FloatType or NoneType
        :return: time from start of run to first of successful pings (or None)
        """
        target, timeout, threshold = self._unpack_parameters(parameters)

        start = now()
        time_limit = start + timeout
        pings = 0
        first = None

        while pings < threshold and now() < time_limit:
            result = self.pinger.run(target)
            if result is not None:
                pings += 1
                if pings == 1:
                    self.logger.info("Pinged target")
                    first = now()
                    first_result = result
            else:
                self.logger.debug("Failed ping")
                pings = 0
                first = None
        if pings == threshold:
            return TTRData(ttr=first - start, rtt=first_result.rtt)
        return
                 
# end TimeToFailure

if __name__ == "__main__":
    ttr = TimeToRecovery()
    print ttr.run("192.168.20.1")
