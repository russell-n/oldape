
# this package
from apetools.baseclass import BaseClass
from baseoperation import BaseOperation 


class DummySetupTest(BaseClass):
    """
    A dummy for an Test 
    """
    def __init__(self):
        super(DummySetupTest, self).__init__()
        return

    def __call__(self, parameters):
        """
        Logs the call
        """
        self.logger.debug("parameters: {0}".format(parameters))
        return
# end class DummyTestSetup


class SetupTest(BaseOperation):
    """
    A class to run every iteration
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `products`: list of products
        """
        super(SetupTest, self).__init__(*args, **kwargs)
        return
# end class SetupTest
