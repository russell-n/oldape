"""
A module to hold the CrashHandler
"""
# python
import traceback

# ttr
from tottest.baseclass import BaseClass
from tottest.commons import storageoutput

class CrashHandler(BaseClass):
    """
    The CrashHandler is called if the entire program crashes and collects crash information.
    """
    def __init__(self, arguments, *args, **kwargs):
        """
        :param:

         - `arguments`: The command line arguments given.
        """
        super(CrashHandler, self).__init__(*args, **kwargs)
        self.arguments = arguments
        return

    def run(self, error):
        """
        This is called when the program crashes.

        :param:

         - `error`: The error returned by the exception
        """
        self.logger.error("The program has crashed. I weep for you.")
        self.logger.error(error)
        output = storageoutput.StorageOutput("CrashReports")
        #with open("crashreport.log", 'w') as f:
        #    traceback.print_exc(file=f)
        f = output.open("crash_report_{t}", '.log')
        traceback.print_exc(file=f)
        separator = "*" * 20
        message = " Crash Report "
        print separator + message + separator
        traceback.print_exc()
        print separator + separator + "*" * len(message)
        return
# end CrashHandler
