"""
An Device Poller Polls the device for changing measurements
"""
#python standard library
from time import time as now, sleep

#apetools
from basedevicepoller import BaseDevicePoller, CSV_JOIN, ZERO


class DevicePollerEnum(object):
    """
    A Holder of rssi-poller constants
    """
    __slots__ = ()
    rssi = 'RSSI'
    devicepoller = 'devicepoller'
# end class DevicePollerEnum

class DevicePoller(BaseDevicePoller):
    """
    A DevicePoller 
    """
    def __init__(self, *args, **kwargs):
        super(DevicePoller, self).__init__(*args, **kwargs)
        return

    @property
    def name(self):
        """
        :return: the name to look for in the logs
        """
        if self._name is None:
            self._name = DevicePollerEnum.devicepoller
        return self._name

    @property
    def expression(self):
        """
        :return: None
        """
        return self._expression

    def run(self):
        """
        :postcondition: the poller is sending rssi values to the output
        """
        interval = self.interval
        if self.use_header:
            self.output.write("timestamp,rssi,noise,bitrate\n")
        while True:
            if self.event is not None:
                self.event.wait()
            start_time = now()
            datum = CSV_JOIN.format(self.timestamp(), self.device.poll())
            self.output.writeline(datum)
            self.logger.debug(datum)
            sleep(max(interval - now() + start_time, ZERO))
        return
# end DevicePoller
