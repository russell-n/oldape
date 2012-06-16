"""
A module to hold the TearDown
"""

from tottest.baseclass import BaseClass


class TearDown(BaseClass):
    """
    The TearDown does whatever needs to be done after the test is completed.
    """
    def __init__(self,tools, *args, **kwargs):
        """
        :param:

         - `tools`: a list of tools to run
        """
        super(TearDown, self).__init__(*args, **kwargs)
        self.tools = tools
        return

    def run(self):
        """
        runs the tools given in the constructor.
        """
        for tool in self.tools:
            tool.run()
        return
# end TearDown
