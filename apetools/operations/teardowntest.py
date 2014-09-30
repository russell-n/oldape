
# this package
from apetools.baseclass import BaseClass
from baseoperation import BaseOperation


class DummyTeardownTest(BaseClass):
    """
    A dummy for a Test teardown
    """
    def __init__(self):
        super(DummyTeardownTest, self).__init__()
        return

    def __call__(self, parameter):
        """
        Logs the parameters
        """
        self.logger.debug("parameters: {0}".format(parameters))
        return
# end class DummyTeardownTest


class TeardownTest(BaseOperation):
    """
    A class to run every iteration
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `products`: list of products
        """
        super(TeardownTest, self).__init__(*args, **kwargs)
        return
# end class SetupTest
