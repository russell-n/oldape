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
from collections import namedtuple
import Queue
import threading


# tottest Libraries
from tottest.baseclass import BaseClass

SPACER = '{0} {1} '
UNKNOWN = "Unknown command: "
EOF = ''

OutputError = namedtuple("OutputError", 'output error')

class NonLocalConnection(BaseClass):
    """
    A non-local connection is the base for non-local connections

    """
    def __init__(self, command_prefix='', *args, **kwargs):
        """
        :param:

         - `command_prefix`: A prefix to prepend to commands (e.g. 'adb shell')
        """
        super(NonLocalConnection, self).__init__(*args, **kwargs)
        # logger is defined in BaseClass but declared here for child-classes
        self._logger = None
        self.command_prefix = command_prefix
        self._queue = None
        self.exc_info = None
        return

    @property
    def queue(self):
        """
        :rtype: Queue.Queue
        :return: the local Queue
        """
        if self._queue is None:
            self._queue = Queue.Queue()
        return self._queue

    def _procedure_call(self, command, arguments='', timeout=None):
        """
        This is provided so it can be overriden by subclasses.
        It is what's called directly by __getattr__ to support LocalConnection.command() calls

        Otherwise it just returns _main()
        """
        return self._main(command, arguments, timeout)
    
    def _main(self, command, arguments='', timeout=None):
        """
        :param:

         - `command`: the command string to execute
         - `arguments`: The arguments for the command

        :return: OutputError named tuple
        """
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
        t = threading.Thread(target=self.run, args=((command,arguments)),
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

    def __str__(self):
        return "{0}".format(self.__class__.__name__)
# end class LocalConnection

