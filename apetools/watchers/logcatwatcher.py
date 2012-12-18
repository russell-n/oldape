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
        self.command = "logcat"
        self._arguments = None
        self._logs = logs
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
            with self.connection.lock:
                output, error = self.connection.ls(self.path)
            self._logs = [log for log in output]
            err = error.readline()
            if len(err):
                self.logger.error(err)
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

    @arguments.setter
    def arguments(self, buffers):
        """
        :param:

        - `buffers`: not used
        """
        return

    def run(self, connection):
        """
        Runs an infinite loop that executes self.command on self.arguments
        Writes the lines to self.output.write()
        """
        with self.connection.lock:
            output, error = self.connection.logcat(self.arguments)
        for line in output:
            self.output.write(line)
            if self.stopped:
                return
        err = error.readline()
        if len(err):
            self.logger.error(err)
        return

    def __str__(self):
        return "{0} {1}".format(self.command, self.arguments)

# end class LogcatWatcher


    
if __name__ == "__main__":
    import sys
    lw = LogcatWatcher(sys.stdout)
    print lw.arguments
    lw.run()
