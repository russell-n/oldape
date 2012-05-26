"""
A module to wrap the python semaphores.
"""
#python
import threading
from itertools import repeat

# tottest
from tottest.baseclass import BaseClass


class Semaphore(BaseClass):
    """
    Implements a Semaphore using Alan Downey's notation.

    This is an unbounded semaphore so it can release more than it has acquired
    """
    def __init__(self, value=1):
        """
        :param:

         - `value`: The number of threads to wait for.
        """
        super(Semaphore, self).__init__()
        self.semaphore = threading.Semaphore(value)
        return

    def wait(self):
        """
        Decrements the semaphore if > 0, waits if it is 0
        """
        self.logger.debug("Acquiring the semaphore")
        self.semaphore.acquire()
        return

    def signal(self, value=1):
        """
        Increments the Semaphore

        :param:

         - `value`: The number of times to increment the Semaphore
        """
        self.logger.debug("releasing {n} times".format(n=value))
        for i in repeat(None, times=value):
            self.semaphore.release()
        return
# end class Semaphore
