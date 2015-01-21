
# this package
from apetools.baseclass import BaseClass
from baseoperation import BaseOperation


class DummyExecuteTest(BaseClass):
    """
    A dummy for an Test 
    """
    def __init__(self):
        super(DummyExecuteTest, self).__init__()
        return

    def __call__(self, parameters, filename_prefix):
        """
        Logs the parameters
        """
        self.logger.info("parameters: {0}".format(parameters))
        self.logger.info("filename_prefix: {0}".format(filename_prefix))
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
        return super(ExecuteTest, self).__init__(*args, **kwargs)
# end class ExecuteTest
