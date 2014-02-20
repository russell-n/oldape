"""
A master event-list holder that adds a timeout
"""
# python standard library
import time

#apetools
from apetools.baseclass import BaseClass

class EventHolder(BaseClass):
    """
    A holder of events that will timeout
    """
    def __init__(self):
        """
        :param:

         - `timeout`: if not None, quit after timeout
        """
        super(EventHolder, self).__init__()
        self._events = None
        return

    @property
    def events(self):
        """
        :return: a list of events
        """
        if self._events is None:
            self._events = []        
        return self._events

    def append(self, event):
        """
        :param:

         - `event`: an event to add

        :postcondition: event appended to self.events
        """
        self.events.append(event)
        return

    def wait(self, timeout=None):
        """
        :param:

         - `timeout`: number of seconds to wait

        :return: True if events set, False on timeout
        """
        end_time = timeout + time.time()
        for event in self.events:
            self.logger.debug(str(event))
            wait_start = time.time()
            event.wait(timeout)
            if time.time() >= end_time:
                return False
            timeout = timeout - (time.time() - wait_start)
        return True
# end class EventHolder
