"""
A module to hold a provider of help messages

The assumption here is that below this file is a structure:

   HELP_FOLDER/<topic>

Where <topic> is the name of a file within which is a variable OUTPUT_VARIABLE
that holds the help string.
"""

#python Libraries
from subprocess import Popen, PIPE, STDOUT
import importlib

#tottest Libraries
from tottest.baseclass import BaseClass
from constants import HELP_FOLDER, BOLD, RESET, HELP_BASE, OUTPUT_VARIABLE

IMPORT_PATH = "{f}.{t}"

class Helper(BaseClass):
    """
    A Helper provides online help
    """
    def __init__(self, *args, **kwargs):
        super(Helper, self).__init__(*args, **kwargs)
        return

    def display(self, topic=None):
        """
        :param:

         - `topic`: The name of a topic to display
        """
        if topic is not None:
            try:
                source = importlib.import_module(IMPORT_PATH.format(f=HELP_FOLDER,
                                                                    t = topic))
            except ImportError:
                print ("\n\tNo help for {0}'{1}'{2} "
                       "yet (tough luck, buddy).\n").format(BOLD,
                                                            topic,
                                                            RESET)
                return
        else:
            source = importlib.import_module(IMPORT_PATH.format(f=HELP_FOLDER,
                                                                t=HELP_BASE))

        try:
            Popen(["less", '-r'],
                  stdin=PIPE,
                  stderr=STDOUT).communicate(input=getattr(source, OUTPUT_VARIABLE))
        except Exception as error:
            print getattr(source, OUTPUT_VARIABLE)
            self.logger.debug(error)
        return
# end class Helper
