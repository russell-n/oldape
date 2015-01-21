
#python
import time
now = time.time

from apetools.baseclass import BaseClass
from apetools.commands import ping


class TimeToFailure(BaseClass):
    """
    A TimeToFailure pings a target until the pings fail.
    """
    def __init__(self, pinger=None, target=None, timeout=300,
                 threshold=5, *args, **kwargs):
        """
        :param:

         - `pinger`: An object to ping a target.
         - `target`: The target address to ping
         - `timeout`: The length of time to try in seconds.
         - `threshold`: The number of consecutive failures to make a fail
        """
        super(TimeToFailure, self).__init__(*args, **kwargs)
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

    def run(self, parameters):
        """
        Pings until failure or timeout.

        :param:

         - `parameters.target`: The address to ping.
         - `parameters.timeout`: The length of time to try (in seconds)
         - `parameters.threshold`: The number of consecutive failures needed to be a failure.

        :rtype: FloatType or NoneType
        :return: time from start of run to first of failed pings (or None)
        """
        if parameters.target is None:
            target = self.target
        else:
            target = parameters.target
        if parameters.timeout is None:
            timeout = self.timeout
        else:
            timeout = parameters.timeout
        if parameters.threshold is None:
            threshold = self.threshold
        else:
            threshold = parameters.threshold

        start = now()
        time_limit = start + timeout
        failures = 0
        first = None

        while failures < threshold and now() < time_limit:
            if self.pinger.run(target):
                failures = 0
                first = None
            else:
                failures += 1
                if failures == 1:
                    first = now()
        if failures == threshold and first is not None:
            return first - start
        return
                 
# end TimeToFailure
