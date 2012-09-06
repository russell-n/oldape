"""
A module to build tear-downs run at the end of a test set.
"""

from tottest.baseclass import BaseClass
from tottest.tools import copyfiles
from tottest.log_setter import LOGNAME
from tottest.proletarians import teardown


class TearDownBuilder(BaseClass):
    """
    A basic tear-down builder that just copies log and config files.
    """
    def __init__(self, configfilename, storage, subdir="logs"):
        """
        :param:

         - `configfilename`: the name of the config file to copy
         - `storage`: A storage object aimed at the data folder.
        """
        super(TearDownBuilder, self).__init__()
        self.configfilename = configfilename
        self.storage = storage
        self.subdir = subdir
        self._configcopier = None
        self._logcopier = None
        self._teardown = None
        return

    @property
    def configcopier(self):
        """
        :return: A file copier aimed at the config file
        """
        if self._configcopier is None:
            self._configcopier = copyfiles.CopyFiles((self.configfilename,),
                                                     self.storage,
                                                     self.subdir)

        return self._configcopier

    @property
    def logcopier(self):
        """
        :return: A file copier aimed at the log file
        """
        if self._logcopier is None:
            self._logcopier = copyfiles.CopyFiles((LOGNAME,),
                                                  self.storage,
                                                  self.subdir)
        return self._logcopier
    
    @property
    def teardown(self):
        """
        :return: A teardown object for the test-operator to run to cleanup
        """
        if self._teardown is None:
            self._teardown = teardown.TeardownSession((self.configcopier,
                                                       self.logcopier))
        return self._teardown
# End class TearDownBuilder
