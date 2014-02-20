# Copyright 2012 Russell Nakamura
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
A module for watchers of kmsg logs.
"""

from apetools.baseclass import BaseClass
from apetools.commons.errors import CommandError
from apetools.threads import threads
from apetools.commons.timestamp import TimestampFormat, TimestampFormatEnums


class LogWatcherError(CommandError):
    """
    An error to raise if something is wrong with the LogWatcher
    """
# end class LogWatcherError


class LogWatcher(BaseClass):
    """
    A LogWatcher watches a log.

    In this case it assumes the log is a file that can be 'cat'-ed and it will block
    """
    def __init__(self, output, event=None, connection=None,  arguments="/proc/kmsg",
                 timestamp_format=TimestampFormatEnums.log,
                 *args, **kwargs):
        """
        :param:

         - `output`: A file-like object to send output to.
         - `event`: A threading event to stop a threaded watcher
         - `connection`: A connection to the Device         
         - `arguments`: The arguments for the command
         - `timestamp_format`: One of the TimestampFormatEnums
        """
        super(LogWatcher, self).__init__(*args, **kwargs)
        self.output = output
        self.event = event
        self.connection = connection
        self.arguments = arguments
        self.timestamp_format = timestamp_format
        self._timestamp = None
        self._logger = None
        self._stop = None
        self._stopped = None
        return

    @property
    def timestamp(self):
        """
        :return: a time-stamper
        """
        if self._timestamp is None:
            self._timestamp = TimestampFormat(self.timestamp_format)
        return self._timestamp

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

    def execute(self):
        """
        This is a hack until the run can be generalized to accept the command (e.g. 'cat')
        
        :return: stdout, stderr
        :postcondition: logcat with arguments sent to the connection
        """
        with self.connection.lock:
            output, error = self.connection.cat(self.arguments)
        return output, error

    def run(self, connection):
        """
        Runs an infinite loop that executes cat on self.arguments
        Writes the lines to self.output.write()
        """
        
        output, error = self.execute()
        for line in output:
            if len(line.strip()):
                self.output.write("{0},{1}".format(self.timestamp.now, line))
            if self.stopped:
                return
        err = error.readline()
        if len(err):
            self.logger.error(err)
        return

    def start(self, connection=None):
        """
        Runs self in a thread.

        :rtype: threading.Thread
        """
        if connection is None:
            connection = self.connection
        if connection is None:
            raise LogWatcherError("Connection not given")
        
        self.thread =  threads.Thread(target=self.run, args=(connection,),
                                      name="LogWatcher {0}".format(self.arguments))
        return self.thread

    def __str__(self):
        return "cat {0}".format(self.arguments)
# end class LogWatcher

class SafeLogWatcher(LogWatcher):
    """
    A SafeLogWatcher uses the connection's lock to protect calls to the connection.
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `lock`: A threading.lock
        """
        super(SafeLogWatcher, self).__init__(*args, **kwargs)
        self.lock = self.connection.lock
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
    
