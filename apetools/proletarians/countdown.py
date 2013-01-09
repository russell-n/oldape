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
A countdown timer for the hortators and operators.
"""
# python libraries
from datetime import datetime as clock
from collections import namedtuple
import heapq
import math

#apetools
from apetools.baseclass import BaseClass

SIXTY = 60.
TWENTY_FOUR = 24

class Times(namedtuple("Times", 'days hours minutes seconds'.split())):
    """
    A Times holds the times after seconds are converted to d,h,m,s
    """
    __slots__ = ()
    def __str__(self):
        return "{0} days, {1} hours, {2} minutes, and {3} seconds".format(self.days,
                                                                          self.hours,
                                                                          self.minutes,
                                                                          self.seconds)
#end class Times


class CountDown(BaseClass):
    """
    A countdown timer
    """
    def __init__(self, total_repetitions=0):
        """
        :param:

         - `total_repetitions`: number of times the operations will be repeated
        """
        super(CountDown, self).__init__()
        self.total_repetitions = total_repetitions
        self.start_time = None
        self._now = None
        self._heap = None
        self._median = None
        self._elapsed = None
        return

    @property
    def elapsed(self):
        """
        :return: timedelta between start time and now (or None if start not set)
        """
        if self.start_time is not None:
            return self.now - self.start_time

    @property
    def median(self):
        """
        :return: dictionary of modulus:function to get median
        """
        if self._median is None:
            self._median = {1:lambda heap:heap[len(heap)/2].total_seconds(),
                  0:lambda heap:(heap[len(heap)/2].total_seconds() +
                                 heap[(len(heap)/2) - 1].total_seconds())/2.}
        return self._median

    @property
    def heap(self):
        """
        :return: list of timedeltas
        """
        if self._heap is None:
            self._heap = []
        return self._heap

    @property
    def now(self):
        """
        :return: datetime.datetime.now()
        """
        return clock.now()

    def start(self):
        """
        :postcondition: self.start_time is now
        """
        self.start_time = clock.now()
        return

    def add(self, start_time):
        """
        :param:

         - `start_time`: datetime object from start of operation

        :postcondition: now - start-time added to the heap
        """
        heapq.heappush(self.heap, self.now - start_time)
        return

    def remaining(self, current_count):
        """
        :param:

         - `current_count`: 0-based index of current operation

        :return: string with estimate of time remaining or None
        """
        remaining = self.total_repetitions - (current_count + 1)
        if not remaining:
            return
        median_time = self.median[len(self.heap)%2](self.heap)
        remaining_time = remaining * median_time
        remaining_time = self.to_time(remaining_time)

    def to_time(self, seconds):
        """
        :param:

         - `seconds`: time in seconds (float)

        :return: days, hours, minutes, seconds
        """
        seconds, minutes = math.modf(seconds/SIXTY)
        minutes, hours = math.modf(minutes/SIXTY)
        hours, days = math.modf(hours/TWENTY_FOUR)
        return Times(days=int(round(days)),
                     hours=int(round(hours * TWENTY_FOUR)),
                     minutes=int(round(minutes * SIXTY)),
                     seconds=int(round(seconds * SIXTY)))

#end class CountDown
