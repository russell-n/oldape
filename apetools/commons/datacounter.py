"""
The Data Counter is meant for event watching.

It tracks the time from its start to its first call.

Intended Sequence::

    d = DataCounter()
    d.start()
    d([data])
    d.stop()

Since it's only counting the data anything passed in to the call is ignored
"""
from collections import namedtuple
import time


class CounterDatum(namedtuple("CounterDatum", "first count")):
    """
    CounterDatum is used to hold the final count:

     - `first`: seconds from start() to first call
     - `count`: total number of calls to DataCounter
    """
# end class CounterDatum
                   

class DataCounter(object):
    """
    The DataCounter counts the number of times it's called
    """
    def __init__(self, missing='na'):
        """
        :param:

         - `missing`: token to use if counter never called
        """
        self.missing = missing
        self.start_time = None
        self.count = 0
        self.first = missing
        self.datum = None
        return

    def start(self):
        """
        :postcondition:

         - `start_time`: set to time()
         - `count`: set to 0
         - `first`: set to missing
        """
        self.start_time = time.time()
        self.count = 0
        self.first = self.missing
        return

    def stop(self):
        """
        :postcondition:

         - `datum`: set to CounterDatum
         - `start_time`: set to None
         - `first`: set to missing
         - `count`: set to 0
        """
        self.datum = CounterDatum(self.first, self.count)
        self.start_time = None
        self.first = self.missing
        self.count = 0
        return
# end class DataCounter
