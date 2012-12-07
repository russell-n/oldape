"""
A place to put classes for operation teardowns
"""

from apetools.baseclass import BaseClass

class DummyTeardownOperation(BaseClass):
    """
    A dummy for an Operation 
    """
    def __init__(self):
        super(DummyTeardownOperation, self).__init__()
        return

    def __call__(self):
        return
# end class DummyOperationSetup
