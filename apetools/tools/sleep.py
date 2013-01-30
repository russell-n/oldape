"""
A module to hold a sleeping class.
"""

# python Libraries
import time
from types import IntType, FloatType

#apetools Libraries
from apetools.baseclass import BaseClass

ONE_SECOND = 1
MESSAGE = "Sleeping for {0} seconds"

class Sleep(BaseClass):
    """
    The sleep provides a verbose sleep.
    """
    def __init__(self, sleep_time=5, *args, **kwargs):
        """
        :param:

         - `sleep_time`: The time (in seconds) to sleep.
        """
        super(Sleep, self).__init__(*args, **kwargs)
        self.sleep_time = int(sleep_time)
        return

    def run(self, sleep_time=None):
        """
        :param:

         - `sleep_time`: The total amount of time to sleep.
        """
        if sleep_time is None or not type(sleep_time) in (IntType, FloatType):
            sleep_time = self.sleep_time

        self.logger.info(MESSAGE.format(sleep_time))
        for t in range(int(sleep_time)):
            print("Wake up in {0} seconds.".format(sleep_time - t))
            time.sleep(1)
        return

    def __call__(self, sleep_time=None):
        """
        An alias for run to make it compatible with the newer interface

        :param:

         - `sleep_time`: The total amount of time to sleep.

        """
        self.run(sleep_time)
# end class Sleep
        
