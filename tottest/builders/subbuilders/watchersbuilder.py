"""
A builder of logwatchers
"""
# python 
from threading import RLock

#tottest
from tottest.baseclass import BaseClass
from tottest.watchers import logwatcher, logcatwatcher
from tottest.watchers import thewatcher

class LogwatchersBuilder(BaseClass):
    """
    Logwatchers Builder builds a master logwatcher
    """
    def __init__(self, paths, buffers, connection, output, lock=None,
                 extension=".log", subdir="logs"):
        """
        :param:

         - `paths`: iterable of paths
         - `buffers`: Iterable of adb buffers
         - `connection`: A connection to the device with the log
         - `output`: object to redirect log to (write to)
         - `lock`: A re-entrant lock to block the connection calls
        """
        super(LogwatchersBuilder, self).__init__()
        self.paths = paths
        self.buffers = buffers
        self.connection = connection
        self.output = output
        self.extension = extension
        self.subdir = subdir
        self._watchers = None
        self._watcher = None
        self._lock = None
        return

    @property
    def lock(self):
        """
        :return: Re-entrant lock
        """
        if self._lock is None:
            self._lock = RLock()
        return self._lock

    @property
    def watchers(self):
        """
        :rtype: ListType 
        :return: A list of watchers
        """
        Watcher = logwatcher.SafeLogWatcher
        ADBWatcher = logcatwatcher.SafeLogcatWatcher
        if self._watchers is None:
            watchers = []
            if self.paths is not None:
                for path in self.paths:
                    name = path.strip("/")
                    name = name.replace("/", "_")
                    watchers.append(Watcher(lock=self.lock,
                                            output=self.output.open(name, extension=self.extension,
                                                                    subdir=self.subdir),
                                            connection=self.connection,
                                            path=path))

            if self.buffers is not None:
                if self.buffers[0] == "all":
                    logs = None
                else:
                    logs = self.buffers
                watchers.append(ADBWatcher(logs=logs,
                                           lock=self.lock,
                                           output=self.output.open("logcatwatcher", extension=self.extension,
                                                                   subdir=self.subdir),
                                           connection=self.connection))
            if len(watchers):
                self._watchers = watchers
        return self._watchers

    @property
    def watcher(self):
        """
        :rtype: TheWatcher
        :return: A master watcher 
        """
        if self._watcher is None:
            self._watcher = thewatcher.TheWatcher(watchers=self.watchers)
        return self._watcher
# end class LogwatchersBuilder
