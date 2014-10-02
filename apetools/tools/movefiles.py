
from apetools.baseclass import BaseClass


class MoveFiles(BaseClass):
    """
    A tool to move files to storage.
    """
    def __init__(self, filenames, storage):
        """
        :param:

         - `filenames`: an iterator of filenames to move
         - `storage`: The mover
        """
        super(MoveFiles, self).__init__()
        self.filenames = filenames
        self.storage = storage
        return

    def run(self):
        """
        Moves the files in filenames to storage.
        """
        for name in self.filenames:
            self.logger.debug("Moving {0}".format(name))
            self.storage.move(name)
        return
# end class MoveFiles
