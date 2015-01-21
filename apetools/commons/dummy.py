
# this package
from apetools.baseclass import BaseClass


LOG_STRING = "{0}.run() called with parameters '{1}'"


class NoOpDummy(BaseClass):
    """
    The NoOpDummy does nothing when asked to do something.
    """
    def __init__(self, name="NoOpDummy"):
        super(NoOpDummy, self).__init__()
        self.name = name
        return

    def run(self, parameters):
        """
        This method logs the parameters and returns.

        It is meant to hide from the caller the fact that it called a non-method.

        This is intended for the Test Operator so it doesn't need to know what it calls
        """
        self.logger.debug(LOG_STRING.format(self.name,
                                            str(parameters)))
        return

    def __call__(self, parameters=None):
        """
        Calls self.run
        """
        self.run(parameters)
# end class NoOpDummy
