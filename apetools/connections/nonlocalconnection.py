## Copyright 2012 Russell Nakamura
##
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.
"""
a module to hold a non-local connection.

The NonLocalConnection takes the command-line command as a property and
the arguments to the command as parameters.

The main difference is that the Local Connection uses forked sub-processes
while the NonLocalConnection is using threads.

The Local Connection has the possibility of more efficiency, but can overload weaker systems
and is generally less robust.
"""

#python Libraries
from StringIO import StringIO
import Queue
import threading


# apetools Libraries
from apetools.baseclass import BaseThreadClass
from localconnection import OutputError 
from apetools.commons import enumerations
SPACER = '{0} {1} '
UNKNOWN = "Unknown command: "
EOF = ''


class NonLocalConnection(BaseThreadClass):
    """
    A non-local connection is the base for non-local connections

    """
    def __init__(self, command_prefix='', lock=None, 
                 operating_system=enumerations.OperatingSystem.linux,
                 path=None,
                 *args, **kwargs):
        """
        :param:

         - `command_prefix`: A prefix to prepend to commands (e.g. 'adb shell')
         - `lock` : A lock to acquire before calls
         - `operating_system`: the operating system
         - `path`: a path setting to add to the path (before :$PATH)
        """
        super(NonLocalConnection, self).__init__(*args, **kwargs)
        # logger is defined in BaseClass but declared here for child-classes
        self._logger = None
        self.command_prefix = command_prefix
        self._lock = lock
        self.path = path
        self._queue = None
        self.operating_system = operating_system
        self.exc_info = None
        return

    @property
    def lock(self):
        """
        :return: a re-entrant lock
        """
        if self._lock is None:
            self._lock = threading.RLock()
        return self._lock
    
    @property
    def queue(self):
        """
        :rtype: Queue.Queue
        :return: the local Queue
        """
        if self._queue is None:
            self._queue = Queue.Queue()
        return self._queue

    def add_path(self, command):
        """
        :param:
        
         - `command`: the name of a command
        :return: command with path additions if given
        """
        if self.path is not None:
            command = "PATH={0}:$PATH;{1}".format(self.path, command)
        return command

    def _procedure_call(self, command, arguments='', timeout=None):
        """
        This is provided so it can be overriden by subclasses.
        It is what's called directly by __getattr__ to support LocalConnection.command() calls

        Otherwise it just returns _main()
        """
        command = self.add_path(command)
        return self._main(command, arguments, timeout)
    
    def _main(self, command, arguments='', timeout=None):
        """
        :param:

         - `command`: the command string to execute
         - `arguments`: The arguments for the command
         - `timeout`: A timeout for the queue when doing a get

        :return: OutputError named tuple
        """
        self.logger.debug("command: '{0}', arguments: '{1}', timeout: '{2}'".format(command,
                                                                                    arguments,
                                                                                    timeout))
        thread = self.start(command, arguments)
        try:
            if self.exc_info:
                raise self.exc_info[1], None, self.exc_info[2]
            return self.queue.get(timeout=timeout)
        except Queue.Empty as error:
            self.logger.debug(error)
            if thread is not None:
                del(thread)
        return OutputError(StringIO(''),StringIO( "'{0} {1}' timed out".format(command, arguments)))

    def run(self, command, arguments):
        """
        Runs the command in a subprocess and puts the output and error on the queue

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.

        :postcondition: OutputError with output and error file-like objects
        """
        raise NotImplementedError("ThreadedConnection is a base class, not a useable class")
        return

    def start(self, command, arguments):
        """
        starts run in a thread

        :return: the thread object
        """
        t = threading.Thread(target=self.run_thread, args=((command,arguments)),
                             name=self.__class__.__name__)
        t.daemon = True
        t.start()
        self.logger.debug(",".join([t.name for t in threading.enumerate() if t.name != "MainThread"]))
        return t

    def __getattr__(self, command):
        """
        The parameters are the same as _procedure_call()
        
        :param:

         - `command`: The command to call.
         - `arguments`: arguments to pass to the command
         - `timeout`: amount of time to wait for the command to return the stdout and stderr files.

        :return: _procedure_call method called with passed-in args and kwargs
        """
        def procedure_call(*args, **kwargs):
            return self._procedure_call(command, *args, **kwargs)
        return procedure_call

    def __call__(self, command, arguments='', timeout=None):
        """
        A pass-through to the _main method to use when the dot-notation doesn't work

        :param:

         - `command`: the command string to execute
         - `arguments`: The arguments for the command
         - `timeout`: A timeout for the queue when doing a get

        :return: OutputError named tuple
        """
        return self._procedure_call(command=command, 
                                    arguments=arguments, timeout=timeout)        

    def __str__(self):
        return "{0}".format(self.__class__.__name__)
# end class LocalConnection

