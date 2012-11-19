"""
A place to put classes to execute a test
"""

from tottest.baseclass import BaseClass

class DummyTeardownTest(BaseClass):
    """
    A dummy for a Test teardown
    """
    def __init__(self):
        super(DummyTeardownTest, self).__init__()
        return

    def __call__(self, parameter):
        return
# end class DummyTeardownTest
