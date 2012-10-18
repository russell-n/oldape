"""
A module for file copiers.
"""

from tottest.baseclass import BaseClass

class CopyFiles(BaseClass):
    """
    A tool to copy files to storage.
    """
    def __init__(self, filenames, storage, subdir=None):
        """
        :param:

         - `filenames`: an iterator of filenames to copy
         - `storage`: The copier.
         - `subdir`: A sub-directory in the storage folder to send copy to
        """
        super(CopyFiles, self).__init__()
        self.filenames = filenames
        self.storage = storage
        self.subdir = subdir
        return

    def run(self):
        """
        Copies the files in filenames to storage.
        """
        for name in self.filenames:
            self.logger.debug("Copying {0}".format(name))
            self.storage.copy(name, self.subdir)
        return
# end class CopyFiles
