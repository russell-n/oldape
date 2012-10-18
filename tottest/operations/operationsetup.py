"""
A place to put classes to setup an operation
"""

from tottest.baseclass import BaseClass

class DummySetupOperation(BaseClass):
    """
    A dummy for an Operation 
    """
    def __init__(self):
        super(DummySetupOperation, self).__init__()
        return

    def __call__(self):
        return
# end class DummyOperationSetup
