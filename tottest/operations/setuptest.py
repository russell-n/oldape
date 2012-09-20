"""
A place to put classes to setup an test
"""

from tottest.baseclass import BaseClass

class DummySetupTest(BaseClass):
    """
    A dummy for an Test 
    """
    def __init__(self):
        super(DummySetupTest, self).__init__()
        return

    def __call__(self, parameters):
        return
# end class DummyTestSetup
