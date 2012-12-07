"""
A module for watchers of logcat logs.
"""

from logwatcher import LogWatcher


class LogcatWatcher(LogWatcher):
    """
    A LogcatWatcher watches the logcat logs.
    """
    def __init__(self, logs=None, *args, **kwargs):
        """
        :param:

         - `output`: A file-like object to send output to.
         - `logs`:  an optional list of logs to use instead of watching all of them.
        """
        super(LogcatWatcher, self).__init__(*args, **kwargs)
        self._logs = logs
        self._arguments = None
        self._logger = None
        self._stop = None
        self._stopped = None
        self.path = "/dev/log/"
        return

    @property
    def logs(self):
        """
        :return: list of logcat buffer names
        """
        if self._logs is None:
            output, error = self.connection.ls(self.path)
            self._logs = [log for log in output]
                
        return self._logs
    
    @property
    def arguments(self):
        """
        :rtype: StringType
        :return: the argument string to pass to the logcat command
        """
        if self._arguments is None:
            logs = (log.rstrip() for log in self.logs)
            logs = (log for log in logs if len(log))
            self._arguments = "-v time" + "".join((" -b " + log for log in logs))
            self.logger.debug("logcat argument string: '{0}'".format(self._arguments))
        return self._arguments
    
    def run(self):
        """
        Runs an infinite loop that reads the tail of the log.
        Writes the lines to self.output.write()
        """
        for line in self.connection.logcat(self.arguments):
            self.output.write(line)
            if self.stopped:
                return
        return
# end class LogcatWatcher


class SafeLogcatWatcher(LogcatWatcher):
    """
    The SafeLogcatWatcher watches a lock to protect the call to the connection.
  
    """
    def __init__(self, lock, *args, **kwargs):
        """
        :param:

         - `lock`: A threading Lock
        """
        super(SafeLogcatWatcher, self).__init__(*args, **kwargs)
        self.lock = lock
        self.path = "/dev/log/"
        return

    @property
    def logs(self):
        """
        :yield: A list of the adb logs.
        """
        with self.lock:
            output, error = self.connection.ls(self.path)

        for line in output:
            yield line
        return
        
    def run(self):
        """
        Runs an infinite loop that reads the tail of the log.
        Writes the lines to self.output.write()
        """
        self.logger.debug("starting the logcat with: {0}".format(self.arguments))
        with self.lock:
            output, error = self.connection.logcat(self.arguments)

        self.logger.debug("Out of the lock")
        for line in output:
            self.output.write(line)
            if self.stopped:
                self.logger.debug("Logcat has been stopped")
                return
        self.logger.debug("Exiting the logcat watcher")
        return
# end class SafeLogcatWatcher
    
if __name__ == "__main__":
    import sys
    lw = LogcatWatcher(sys.stdout)
    print lw.arguments
    lw.run()
