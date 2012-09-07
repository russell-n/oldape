"""
a module to hold a threaded connection.

The LocalConnection takes the command-line command as a property and
the arguments to the command as parameters.

e.g.

    `lc = LocalConnection()`
    `output = lc.ls('-l')`
    `print output.output`

prints the output of the `ls -l` command line command

The localConnection uses Subprocess, while the LocalNixConnection uses
pexepect. If the LocalConnection is hanging because the output is being
buffered, use the LocalNixConnection instead.
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

class ThreadedConnection(BaseClass):
    """
    A threaded connection is the base for non-local connections

    """
    def __init__(self, command_prefix='', *args, **kwargs):
        """
        :param:

         - `command_prefix`: A prefix to prepend to commands (e.g. 'adb shell')
        """
        super(ThreadedConnection, self).__init__(*args, **kwargs)
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
        :param:

         - `command`: The command to call.
        """
        def procedure_call(*args, **kwargs):
            return self._procedure_call(command, *args, **kwargs)
        return procedure_call

    def __str__(self):
        return "{0}".format(self.__class__.__name__)
# end class LocalConnection

