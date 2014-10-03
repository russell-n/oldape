
#python standard library
from time import time as now, sleep

#apetools
from apetools.parsers import oatbran
from basepollster import BasePollster, CSV_JOIN, ZERO


class RssiPollerEnum(object):
    """
    A Holder of rssi-poller constants
    """
    __slots__ = ()
    rssi = 'RSSI'
    rssipoller = 'rssipoller'
# end class RssiPollerEnum


class RssiPoller(BasePollster):
    """
    A DevicePoller for RSSI
    """
    def __init__(self, *args, **kwargs):
        super(RssiPoller, self).__init__(*args, **kwargs)
        return

    @property
    def name(self):
        """
        :return: the name to look for in the logs
        """
        if self._name is None:
            self._name = RssiPollerEnum.rssipoller
        return self._name

    @property
    def expression(self):
        """
        :return: uncompiled expression to match RSSI
        """
        if self._expression is None:
            self._expression = (oatbran.NAMED(n=RssiPollerEnum.rssi,
                                              e=oatbran.INTEGER))
        return self._expression

    def run(self):
        """
        :postcondition: the poller is sending rssi values to the output
        """
        interval = self.interval
        if self.use_header:
            self.output.write("timestamp,rssi\n")
        while True:
            if self.event is not None:
                self.event.wait()
            start_time = now()
            datum = CSV_JOIN.format(self.timestamp(), self.device.rssi)
            self.output.writeline(datum)
            self.logger.debug(datum)
            sleep(max(interval - now() + start_time, ZERO))
        return
# end RssiPoller
