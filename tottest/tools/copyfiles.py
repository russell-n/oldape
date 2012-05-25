"""
A module for file copiers.
"""

from timetorecovertest.baseclass import BaseClass

class CopyFiles(BaseClass):
    """
    A tool to copy files to storage.
    """
    def __init__(self, filenames, storage):
        """
        :param:

         - `filenames`: an iterator of filenames to copy
         - `storage`: The copier.
        """
        super(CopyFiles, self).__init__()
        self.filenames = filenames
        self.storage = storage
        return

    def run(self):
        """
        Copies the files in filenames to storage.
        """
        for name in self.filenames:
            self.logger.debug("Copying {0}".format(name))
            self.storage.copy(name)
        return
# end class CopyFiles
