"""
A lock to block a semaphore.

This is primarily intended to enable::

 with Lock(mutex):
     pass
"""

from contextlib import contextmanager

@contextmanager
def lock(semaphore):
    """
    Provides an alternative locking mechanism for the `with`
    """
    try:
        semaphore.wait()
        yield
    finally:
        semaphore.signal()
    return

class Lock(object):
    """
    A Lock defines __enter__ and __exit__ methods.
    """
    def __init__(self, semaphore):
        """
        :param:

         - `semaaphore`: A Semaphore with `wait` and `signal` methods.
        """
        self.semaphore = semaphore
        return

    def __enter__(self):
        """
        calls the Semaphore's wait() method
        """
        self.semaphore.wait()
        return

    def __exit__(self):
        """
        Calls the Semaphore's signal() method.
        """
        self.semaphore.signal()
        return
# end class Lock
