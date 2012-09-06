"""
The Storage Broadcaster decorates the Broadcaster to change the file target.
"""
from broadcaster import Broadcaster


class StorageBroadcaster(Broadcaster):
    """
    The Storage Broadcaster opens a new file on each setup.
    """
    def __init__(self, storage, extension, *args, **kwargs):
        """
        :param:

         - `storage`: a Storage object pre-loaded with the path
         - `extension`: an extension to give to the storage
         - `receivers`: an iterable container of subscribers to the broadcast.
        """
        super(StorageBroadcaster, self).__init__(*args, **kwargs)
        self.storage = storage
        self.extension = extension
        return

    def set_up(self, filename):
        """
        :param:

         - `filename`: the name of a file to open

        :postcondition: opened storage with filename sent to parent `set_up`
        """
        output = self.storage.open(filename, extension=self.extension)
        super(StorageBroadcaster, self).set_up(output)
        return
# end class Storage Broadcaster
