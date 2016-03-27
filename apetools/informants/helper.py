
#python Libraries
from subprocess import Popen, PIPE, STDOUT

# third-party
from yapsy.PluginManager import PluginManager

#apetools Libraries
from apetools.baseclass import BaseClass
from constants import HELP_FOLDER, BOLD, RESET, HELP_BASE, OUTPUT_VARIABLE

IMPORT_PATH = "{f}.{t}"

class Helper(BaseClass):
    """
    A Helper provides online help
    """
    def __init__(self, *args, **kwargs):
        super(Helper, self).__init__(*args, **kwargs)
        self._plugin_manager = None
        return

    @property
    def plugin_manager(self):
        if self._plugin_manager is None:
            self._plugin_manager = PluginManager()
            self._plugin_manager.setPluginPlaces([HELP_FOLDER])
            self._plugin_manager.collectPlugins()
        return self._plugin_manager

    def display(self, topic=None):
        """
        :param:

         - `topic`: The name of a topic to display
        """
        if topic is not None:
            source = self.plugin_manager.getPluginByName(topic)
                                                                   

            #print ("\n\tNo help for {0}'{1}'{2} "
            #           "yet (tough luck, buddy).\n").format(BOLD,
            #                                                topic,
            #                                                RESET)
            return
        else:
            source = self.plugin_manager.getPluginByName(HELP_BASE)

        try:
            Popen(["less", '-r'],
                  stdin=PIPE,
                  stderr=STDOUT).communicate(input=source.output)
        except Exception as error:
            print(getattr(source.output))
            self.logger.debug(error)
        return
# end class Helper

#standard library
import unittest

class TestHelper(unittest.TestCase):
    def test_constructor(self):
        h = Helper()