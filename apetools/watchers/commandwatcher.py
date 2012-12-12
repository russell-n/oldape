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
A module to repeatedly call a bash command and log its output

This requires a regular expression to match
"""
# python standard library
import re
from time import time, sleep
import threading

from apetools.baseclass import BaseClass
from apetools.commons.timestamp import TimestampFormat

class CommandWatcher(BaseClass):
    """
    A class to call a command and save a csv using the output
    """
    def __init__(self, output, command, expression, connection=None, interval=1):
        """
        :param:

        - `output`: A writeable file-like object
        - `interface`: The name of the interface to watch
        - `interval`: seconds between samples
        - `connection`: the connection to the device to watch
        - `command`: string with command and arguments
        - `expression`: A regular expression with groups to match the output
        """
        super(CommandWatcher, self).__init__()
        self.output = output
        self.interval = interval
        self.connection = connection
        self.expression = expression
        self._timestamp = None
        self.command = command
        self.stopped = False
        return

    @property
    def expression(self):
        """
        :return: compiled regular expression to match the interface output line
        """
        return self._expression

    @expression.setter
    def expression(self, expr):
        """
        :param:

         - `expr`: A string regular expression to match the file output

        :postcondition: self._expr is a compiled regular expression        
        """
        self._expression = re.compile(expr)
        return
    
    @property
    def timestamp(self):
        """
        :return: timestamper 
        """
        if self._timestamp is None:
            self._timestamp = TimestampFormat()
        return self._timestamp
    
    def stop(self):
        """
        :postcondition: `self.stopped` is True
        """
        self.stopped = True
        return


    def __call__(self, connection=None):
        """
        This is an adapter to the start interface

        :param:

         - `connection`: a connection to the device
        """
        if connection is None:
            connection = self.connection
        self.start(connection)
        return
    
    def start(self):
        """
        :postcondition: `run` method running in a thread
        """
        t = threading.Thread(target=self.run, name="commandwatcher")
        t.daemon = True
        t.start()
        return
    
    def run(self):
        start = time()

        while not self.stopped:                
            start = time()
            matches = []
            output, error = self.connection.sh(self.command)
            for line in output:
                self.logger.debug(line)
                match = self.expression.search(line)
                if match:
                    for value in match.groups():
                        matches.append(value)
            self.output.write("{0},{1}\n".format(self.timestamp.now, ','.join(matches)))
            try:
                sleep(self.interval - (time() - start))
            except IOError:
                self.logger.debug("cat {0} took more than one second".format(self.name))

        return
# end class CommandWatcher

                                  
if __name__ == "__main__":
    from apetools.connections.sshconnection import SSHConnection
    import sys                                  
    c = SSHConnection("portege", "portegeadmin")
    p = ProcnetdevWatcher(sys.stdout, c, "wlan0")
    p()
