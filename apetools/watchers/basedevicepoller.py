"""
A module to hold the basic device-poller, a watcher that queries the device at specific intervals
"""

# python standard library
from abc import ABCMeta, abstractmethod, abstractproperty
import re

# apetools
from apetools.baseclass import BaseClass
from apetools.commons.timestamp import TimestampFormat, TimestampFormatEnums
from apetools.threads.threads import Thread


#constants
CSV_JOIN = "{0},{1}"
ZERO = 0

class BaseDevicePoller(BaseClass):
    """
    An abstract class to base Device-Pollsters on.
    """
    __metaclass__ = ABCMeta
    def __init__(self, device, output, expression=None, interval=1,
                 timestamp=None, name=None, event=None):
        """
        :param:

         - `device`: a device to query
         - `output`: a file to send output to
         - `expression`: an expression to match the output
         - `interval`: time between polling
         - `timestamp`: a timestamp creator
         - `name`: Name to use in the logs
         - `event`: An event which if set starts the polling
        """
        super(BaseDevicePoller, self).__init__()
        self._logger = None
        self.device = device
        self.output = output
        self._expression = expression
        self.interval = interval
        self.event = event
        self._name = name
        self._timestamp = timestamp
        self._regex = None
        return

    @abstractproperty
    def name(self):
        """
        :return: the name for logging
        """
        return self._name

    @abstractproperty
    def expression(self):
        """
        :return: uncompiled expression to match the output
        """
        return self._expression

    @property
    def timestamp(self):
        """
        :return: timestamp creator
        """
        if self._timestamp is None:
            self._timestamp = TimestampFormat(TimestampFormatEnums.log)
        return self._timestamp

    @property
    def regex(self):
        """
        :return: a compiled regular expression to match the output
        """
        if self._regex is None:
            self._regex = re.compile(self.expression)        
        return self._regex

    @abstractmethod
    def run(self):
        """
        The method to poll the device
        """
        return

    def start(self):
        """
        :postcondition: self.thread contains the run() thread
        """
        self.thread = Thread(target=self.run, name=self.name)
        return

    def __call__(self):
        """
        A pass-through to start
        """
        self.start()
        return
# end class BaseDevicePoller
    
