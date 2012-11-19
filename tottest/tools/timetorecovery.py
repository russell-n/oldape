"""
The time to failure pings a target until the pings fail.
"""
#python
import time
now = time.time

from collections import namedtuple

# tottest libraries
from tottest.baseclass import BaseClass
from tottest.commons.errors import CommandError
from tottest.commands import ping

class TTRData(namedtuple("TTRData", "ttr rtt")):
    """
    A TTRData holds the TimeToRecovery data
    """
    __slots__ = ()

    def __str__(self):
        return "ttr={0},rtt={1}".format(self.ttr, self.rtt)


class TimeToRecovery(BaseClass):
    """
    A TimeToRecovery pings a target until the pings succeeed.
    """
    def __init__(self, nodes, pinger=None, target=None, timeout=300,
                 threshold=5):
        """
        :param:

         - `nodes`: A dictionary of id:device pairs
         - `pinger`: An object to ping a target.
         - `target`: The target address to ping
         - `timeout`: The length of time to try in seconds.
         - `threshold`: The number of consecutive pings to make a recovery
        """
        super(TimeToRecovery, self).__init__()
        self.nodes = nodes
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
            self._pinger = ping.PingCommand()
        return self._pinger

    def _unpack_parameters(self, parameters):
        try:
            target = parameters.target.parameters
        except AttributeError:
            target = self.target
        try:
            timeout = parameters.timeout.parameters
        except AttributeError:
            timeout = self.timeout
        try:
            threshold = parameters.threshold.parameters
        except AttributeError:
            threshold = self.threshold
        return target, timeout, threshold
        
    def run(self, parameters=None, connection=None):
        """
        Pings until failure or timeout.

        :param:

         - `parameters.target`: The address to ping.
         - `parameters.timeout`: The length of time to try (in seconds)
         - `parameters.threshold`: The number of consecutive pings needed to be a success.
         - `connection`: The connection to the source of the ping

        :rtype: FloatType or NoneType
        :return: time from start of run to first of successful pings (or None)
        """
        target, timeout, threshold = self._unpack_parameters(parameters)
        self.logger.info(("{pinger}: Waiting for {target} to return {threshold} pings"
                          " (up to {timeout} seconds)").format(target=target, threshold=threshold,
                                                               timeout=timeout, pinger=connection))
        start = now()
        time_limit = start + timeout
        pings = 0
        first = None

        while pings < threshold and now() < time_limit:
            result = self.pinger(target, connection)
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

    def __call__(self, parameters):
        """
        :param:

         - `parameters`: namedtuple with nodes and targets attribute

        :return: TTRData
        :raises: CommandError if unable to recover
        """
        ttr =  self.run(parameters, self.nodes[parameters.nodes.parameters].connection)
        self.logger.info("TTR: {0}".format(ttr))
        if ttr is None:
            raise CommandError("Unable to ping {0}".format(parameters.target.parameters))
        return ttr
# end TimeToRecovery

if __name__ == "__main__":
    ttr = TimeToRecovery()
    print ttr.run("192.168.20.1")
