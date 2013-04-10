"""
A Module to hold a teardown for a single iteration.
"""

from apetools.baseclass import BaseClass
from apetools.tools import teardowniteration


class TeardownIterationBuilder(BaseClass):
    """
    The TeardownIteration builder builds a single TeardownIteration
    """
    def __init__(self):
        """
        """
        super(TeardownIterationBuilder, self).__init__()
        self._teardowniteration = None
        return

    @property
    def teardowniteration(self):
        """
        :return: A tear-down for an iteration
        """
        if self._teardowniteration is None:
            self._teardowniteration = teardowniteration.TeardownIteration()
        return self._teardowniteration
# end class TeardownIterationBuilder


