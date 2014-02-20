
from apetools.watchers.logwatcher import LogWatcher


class LogFollower(LogWatcher):
    """
    A file-follower
    """
    def __init__(self, *args, **kwargs):
        """
        Takes whatever parameters the LogFollower does
        """
        super(LogFollower, self).__init__(*args, **kwargs)
        return

    def execute(self):
        """
        Overrides LogWatcher.execute to use tail

        :return: stdout, stderr from self.connection
        """
        with self.connection.lock:
            output, error = self.connection.tail(' -f {0}'.format(self.arguments))
        return output, error
