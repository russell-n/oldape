"""
A place to put classes to execute a test
"""

from tottest.baseclass import BaseClass
from baseoperation import BaseOperation


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

class ExecuteTest(BaseOperation):
    """
    A caller of tests
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `products`: list of products
        """
        super(ExecuteTest, self).__init__(*args, **kwargs)
        return
# end class ExecuteTest
                  
