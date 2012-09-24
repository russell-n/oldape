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

class SetupTest(BaseClass):
    def __init__(self, products):
        """
        :param:

         - `products`: list of products
        """
        super(SetupTest, self).__init__()
        self.products = products
        return

    def __call__(self, parameters):
        """
        :parameters: namedtuple that has the parameters to run the setup
        """
        for product in self.products:
            product(parameters)
        return
# end class SetupTest
