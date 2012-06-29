"""
The dummy is meant to sit in when an object with a run method is called but not needed.
"""

from tottest.baseclass import BaseClass


class NoOpDummy(BaseClass):
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
        self.logger.debug("{0}.run() called with parameters '{1}'".format(str(parameters)))
        return

# end class NoOpDummy
