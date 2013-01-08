## Copyright 2012 Russell Nakamura
##
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.
"""
A Base for both pollsters and intermittent file watchers
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


class BasePollster(BaseClass):
    """
    An abstract class to base Device-Pollsters on.
    """
    __metaclass__ = ABCMeta
    def __init__(self, device, output, expression=None, interval=1,
                 timestamp=None, name=None, event=None, use_header=True):
        """
        :param:

         - `device`: a device to query
         - `output`: a file to send output to
         - `expression`: an expression to match the output
         - `interval`: time between polling
         - `timestamp`: a timestamp creator
         - `name`: Name to use in the logs
         - `event`: An event which if set starts the polling
         - `use_header`: If True, prepend header to output
        """
        super(BasePollster, self).__init__()
        self._logger = None        
        self.device = device
        self.output = output
        self._expression = expression
        self.interval = interval
        self.event = event
        self.use_header = use_header
        self._name = name
        self._timestamp = timestamp
        self._regex = None
        return

    @abstractproperty
    def name(self):
        """
        :return: the name for logging (or the name of the file)
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
# end class BasePollster
