"""
A place to put classes to execute a test
"""

from tottest.baseclass import BaseClass

class DummyExecuteTest(BaseClass):
    """
    A dummy for an Test 
    """
    def __init__(self):
        super(DummyExecuteTest, self).__init__()
        return

    def __call__(self, parameters):
        return
# end class DummyExecuteTest
