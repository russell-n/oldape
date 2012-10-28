"""
A module for watchers of kmsg logs.
"""

from tottest.baseclass import BaseClass
from tottest.connections import adbconnection
from tottest.threads import threads


class LogWatcher(BaseClass):
    """
    A LogWatcher watches a log.

    In this case it assumes the log is a file that can be 'catted'
    """
    def __init__(self, output, event=None, connection=None, path="/proc/kmsg",
                 command="cat", *args, **kwargs):
        """
        :param:

         - `output`: A file-like object to send output to.
         - `event`: A threading event to stop a threaded watcher
         - `connection`: A connection to the Device         
         - `path`: The full path to the log.
         - `command`: the command to watch the log (change to `tail -f` if needed)
        """
        super(LogWatcher, self).__init__(*args, **kwargs)
        self.output = output
        self.event = event
        self._connection = connection
        self.path = path
        self.command = command
        self._arguments = None
        self._logger = None
        self._stop = None
        self._stopped = None
        return

    @property
    def stop(self):
        """
        This sets the event (to match the Watcher).

        """
        if self.event is not None:
            #self.event.set()
            pass
        return 

    @property
    def stopped(self):
        """
        :rtype: Boolean
        :return: True if self.stop is set.
        """
        if self.event is not None:
            return self.event.is_set()
        return False
    
    @property
    def connection(self):
        """
        :rtype: ADBShellConnection
        :return: An adb-shell connection
        """
        if self._connection is None:
            self._connection = adbconnection.ADBShellConnection()
        return self._connection
        
    @property
    def arguments(self):
        """
        :rtype: StringType
        :return: the argument string to pass to the logcat command
        """
        if self._arguments is None:
            self._arguments = self.path
            self.logger.debug("log argument string: '{0}'".format(self._arguments))
        return self._arguments
         
    def run(self):
        """
        Runs an infinite loop that reads the tail of the log.
        Writes the lines to self.output.write()
        """
        for line in self.connection.bash("{0} {1}".formac(self.command, self.arguments)):
            self.output.write(line)
            if self.stopped:
                return
        return

    def start(self):
        """
        Runs self in a thread.

        :rtype: threading.Thread
        """
        self.thread =  threads.Thread(self.run)
        return self.thread
# end class LogWatcher

class SafeLogWatcher(LogWatcher):
    """
    A SafeLogWatcher uses a lock to protect calls to the connection.
    """
    def __init__(self, lock, *args, **kwargs):
        """
        :param:

         - `lock`: A threading.lock
        """
        super(SafeLogWatcher, self).__init__(*args, **kwargs)
        self.lock = lock
        return

    def run(self):
        """
        Runs an infinite loop that reads the tail of the log.
        Writes the lines to self.output.write()
        """
        self.logger.debug("Catting the file: {0}".format(self.arguments))
        with self.lock:
            output, error = self.connection.cat(self.arguments)
        self.logger.debug("Out of the catting")
        for line in output:
            self.output.write(line)
            if self.stopped:
                self.logger.debug("logwatcher stopped")
                return
        self.logger.debug("Exiting the SafeLogWatcher")
        return
# end class SafeLogWatcher

    
if __name__ == "__main__":
    import sys
    kw = LogWatcher(sys.stdout)
    print kw.arguments
    kw.run()
