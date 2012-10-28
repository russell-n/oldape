"""
A filterer for pipelines
"""

#Python
import re

# tottest
from tottest.baseclass import BaseClass

class Filterer(BaseClass):
    """
    A Filterer filters out strings that don't match an expression.
    """
    def __init__(self, expression, target, event=None):
        """
        :param:

         - `expression`: A regular expression.
         - `target`: a target to send matching strings to
         - `event`: an Event to activate flow through the filter
        """
        super(Filterer, self).__init__()
        self.expression = expression
        self.target = target
        self._event = event
        self._regex = None
        return

    @property
    def event(self):
        """
        :return: threading event
        """
        if self._event is None:
            self._event = DummyEvent()
        return self._event
    
    @property
    def regex(self):
        """
        :return: A compiled regular expression to match
        """
        if self._regex is None:
            self._regex = re.compile(self.expression)
        return self._regex

    def __call__(self, line):
        """
        This only runs if the event is set
        
        :param:

         - `line`: A string to check before propagating
        """
        if not self.event.is_set():
            return
        match = self.regex.search(line)
        if match:
            self.logger.debug("UnFiltered: {0}".format(line))
            self.target(line)
        return
# end class Filter

class DummyEvent(object):
    def __init__(self):
        return

    def is_set(self):
        """
        Always returns True to leave the filter running

        :rtype: Boolean
        :return: True
        """
        return True
