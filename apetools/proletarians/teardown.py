
from apetools.baseclass import BaseClass


class TeardownSession(BaseClass):
    """
    The TearDown does whatever needs to be done after the test is completed.

    It iterates over the `tools` passed in to the constructor.
    Each tool's `run` method is called.
    Choosing tools and ordering them defines the TeardownSession algorithm.
    """
    def __init__(self,tools, *args, **kwargs):
        """
        :param:

         - `tools`: a list of tools to run
        """
        super(TeardownSession, self).__init__(*args, **kwargs)
        self.tools = tools
        return

    def run(self):
        """
        Calls the run() method for each tool in `tools`

        """
        for tool in self.tools:
            tool.run()
        return
# end TeardownSession
