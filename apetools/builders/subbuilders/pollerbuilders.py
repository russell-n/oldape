
from apetools.baseclass import BaseClass
from apetools.commons.errors import ConfigurationError
from apetools.commons.storageoutput import APPEND
from apetools.watchers.rssipoller import RssiPoller
from apetools.watchers.devicepoller import DevicePoller
from apetools.watchers.procpollster import ProcnetdevPollster
from apetools.watchers.procpollster import CpuPollster


class PollerBuilderError(ConfigurationError):
    """
    An exception to raise of the poller can't be built
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
        self._name = name
        self.output = output
        self._product = None
        self._output_file = None
        self._filename = None
        self._subdir = None
        self._interval = None
        self._use_header = None
        return

    @property
    def name(self):
        """
        A getter for name (identifier)
        """
        return self._name

    @property
    def use_header(self):
        """
        :return: True if this is a new file
        """
        if self._use_header is None:
            self._use_header = not self.output.is_file(filename=self.filename,
                                                       subdir=self.subdir)
        return self._use_header


    @property
    def subdir(self):
        """
        :return: name of subdirectory for output file
        """
        if self._subdir is None:
            if hasattr(self.parameters, 'subdir'):
                self._subdir = self.parameters.subdir
            else:
                self._subdir = 'logs'
        return self._subdir

    @property
    def filename(self):
        """
        :return: name for output file
        """
        if self._filename is None:
            self._filename = ("{0}_{1}".format(self.parameters.type, self.name.replace('/', '') +
                              ".log"))
        return self._filename

    @property
    def output_file(self):
        """
        :return: opened file to send output to
        """
        if self._output_file is None:
            self._output_file = self.output.open(self.filename,
                                                 subdir=self.subdir,
                                                 mode=APPEND)
        return self._output_file

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
# end class BasePollerBuilder


class ProcnetdevPollsterBuilder(BasePollerBuilder):
    """
    A builder of network interface pollers
    """
    def __init__(self, *args, **kwargs):
        super(ProcnetdevPollsterBuilder, self).__init__(*args, **kwargs)
        self._interval = None
        return

    @property
    def product(self):
        """
        :return: rssi-poller
        """
        if self._product is None:
            # self.output_file creates it so this check has to come first
            use_header = self.use_header
            self._product = ProcnetdevPollster(device=self.node,
                                               output=self.output_file,
                                               interval=self.interval,
                                               interface=self.node.interface,
                                               use_header=use_header)
        return self._product
# end class ProcdevnetPollsterBuilder


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
                                       interval=self.interval,
                                       use_header=self.use_header)
        return self._product
# end class RssiPollerBuilder


class DevicePollerBuilder(BasePollerBuilder):
    """
    A builder of rssi-pollers
    """
    def __init__(self, *args, **kwargs):
        super(DevicePollerBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def product(self):
        """
        :return: device-poller
        """
        if self._product is None:
            self._product = DevicePoller(device=self.node,
                                         output=self.output_file,
                                         interval=self.interval,
                                         use_header=self.use_header)
        return self._product
# end class DevicePollerBuilder


class CpuPollsterBuilder(BasePollerBuilder):
    """
    A builder of cpu pollers
    """
    def __init__(self, *args, **kwargs):
        super(CpuPollsterBuilder, self).__init__(*args, **kwargs)
        self._interval = None
        return

    @property
    def product(self):
        """
        :return: cpu-poller
        """
        if self._product is None:
            # self.output_file creates it so this check has to come first
            use_header = self.use_header
            self._product = CpuPollster(device=self.node,
                                        output=self.output_file,
                                        interval=self.interval,
                                        use_header=use_header)
        return self._product
# end class CpuPollsterBuilder
