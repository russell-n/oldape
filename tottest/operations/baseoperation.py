"""
A module to hold the common elements for operations
"""

from tottest.baseclass import BaseClass

class DummyOperation(BaseClass):
    """
    A dummy for an Test 
    """
    def __init__(self):
        super(DummyOperation, self).__init__()
        return

    def __call__(self, parameters):
        return
# end class DummyOperation


class BaseOperation(BaseClass):
    """
    A Base operations holds the common elements operations
    """
    def __init__(self, products):
        """
        :param:

         - `products`: list of tools to call
        """
        super(BaseOperation, self).__init__()
        self._logger = None
        self.products = products
        return

    def __call__(self, parameters):
        """
        :parameters: namedtuple with settings to run the operation
        """
        for product in self.products:
            product(parameters)
        return
# end class BaseOperation
    
