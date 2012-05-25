"""
A module to hold actions for the end of a single test-iteration.
"""

from timetorecovertest.baseclass import BaseClass
from sleep import Sleep

class TeardownIteration(BaseClass):
    """
    A TeardownIteration does what's needed after a single iteration.
    """
    def __init__(self, *args, **kwargs):
        super(TeardownIteration, self).__init__(*args, **kwargs)
        self._sleep = None
        return

    @property
    def sleep(self):
        """
        :rtype: sleep.Sleep
        :return: Blocking countdown-timer
        """
        if self._sleep is None:
            self._sleep = Sleep()
        return self._sleep

    def run(self, parameters):
        """
        :param:

         - `parameters`: object with `recovery_time` property
        """
        self.sleep.run(parameters.recovery_time)
        return
# end TeardownIteration
