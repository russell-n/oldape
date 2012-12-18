"""
A module to build device pollers
"""

from apetools.baseclass import BaseClass
from apetools.commons.errors import ConfigurationError

from apetools.watchers.rssipoller import RssiPoller
from apetools.watchers.devicepoller import DevicePoller

class PollerBuilderError(ConfigurationError):
    """
    """
# end PollerBuilderError


class BasePollerBuilder(BaseClass):
    """
    A class to base other builders on
    """
    def __init__(self, node, parameters, output,
                 name=None, event=None):
        """
        :param:

         - `node`: device to watch        
         - `parameters`: named tuple built from config file
         - `output`: storageobject to send output to
         - `name`: a name to add to the output file
         - `event`: event to watch to decide when to stop
        """
        super(BasePollerBuilder, self).__init__()
        self._logger = None
        self.node = node
        self.parameters = parameters
        self.event = event
        self.name = name
        self.output = output
        self._product = None
        self._output_file = None
        return

    @property
    def output_file(self):
        """
        :return: opened file to send output to
        """
        if self._output_file is None:
            prefix = "{0}_{1}".format(self.parameters.type, self.name)
            self._output_file = self.output.open("{0}.log".format(prefix),
                                                 subdir="logs")
        return self._output_file

# end class BasePollerBuilder


class RssiPollerBuilder(BasePollerBuilder):
    """
    A builder of rssi-pollers
    """
    def __init__(self, *args, **kwargs):
        super(RssiPollerBuilder, self).__init__(*args, **kwargs)
        self._interval = None
        return

    @property
    def interval(self):
        """
        :return: time between polls
        """
        if self._interval is None:
            if hasattr(self.parameters, "interval"):
                self._interval = float(self.parameters.interval)
            else:
                self._interval = 1
        return self._interval

    @property
    def product(self):
        """
        :return: rssi-poller
        """
        if self._product is None:
            self._product = RssiPoller(device=self.node,
                                       output=self.output_file,
                                       interval=self.interval)
        return self._product
# end class RssiPollerBuilder

class DevicePollerBuilder(BasePollerBuilder):
    """
    A builder of rssi-pollers
    """
    def __init__(self, *args, **kwargs):
        super(DevicePollerBuilder, self).__init__(*args, **kwargs)
        self._interval = None
        return

    @property
    def interval(self):
        """
        :return: time between polls
        """
        if self._interval is None:
            if hasattr(self.parameters, "interval"):
                self._interval = float(self.parameters.interval)
            else:
                self._interval = 1
        return self._interval

    @property
    def product(self):
        """
        :return: device-poller
        """
        if self._product is None:
            self._product = DevicePoller(device=self.node,
                                         output=self.output_file,
                                         interval=self.interval)
        return self._product
# end class DevicePollerBuilder
