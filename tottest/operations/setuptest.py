"""
A place to put classes to setup an test
"""

from tottest.baseclass import BaseClass
from baseoperation import BaseOperation 

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

class SetupTest(BaseOperation):
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `products`: list of products
        """
        super(SetupTest, self).__init__(*args, **kwargs)
        return
# end class SetupTest
