"""
a module to hold a local connection.

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
from subprocess import PIPE, Popen
from StringIO import StringIO
import shlex
from collections import namedtuple
import Queue
import threading
import os

# Third-party Libraries
try:
    import pexpect
except ImportError as error:
    print error

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.commons.errors import ConnectionError
from tottest.commons.readoutput import StandardOutput
from tottest.commons.enumerations import OperatingSystem

SPACER = '{0} {1} '
UNKNOWN = "Unknown command: "
EOF = ''

OutputError = namedtuple("OutputError", 'output error')

class LocalConnection(BaseClass):
    """
    A local connection talks to a local command-line shell.

    """
    def __init__(self, command_prefix='', *args, **kwargs):
        """
        :param:

         - `command_prefix`: A prefix to prepend to commands (e.g. 'adb shell')
        """
        super(LocalConnection, self).__init__(*args, **kwargs)
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

    def _rpc(self, command, arguments='', timeout=None):
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
        try:
            if len(self.command_prefix):
                command = SPACER.format(self.command_prefix, command)
            process = Popen(shlex.split(SPACER.format(command, arguments)),
                        stdout=PIPE, stderr=PIPE)

            self.queue.put(OutputError(process.stdout, process.stderr))
        except OSError as error:
            import sys
            self.exc_info = sys.exc_info()
            self.logger.error(error)
            #raise ConnectionError(UNKNOWN + command)
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
        return t

    def add_paths(self, paths):
        """
        :param:

         - `paths`: A list of directories to add to the path

        :postcondition: The command_prefix adds the paths to the PATH
        """
        output, error = self._main("echo", "'$PATH'", timeout=1)
        if self.exc_info:
            raise ConnectionError, self.exc_info[1], self.exc_info[2]
        default = output.readline().rstrip()
        self.logger.debug("Starting Path: {0}".format(default))
        default_list = default.split(":")
        paths = ":".join([path for path in paths if path not in default_list])
        self.logger.debug("Adding paths: {0}".format(paths))
        if len(self.command_prefix):
            self.command_prefix += " PATH={0}:{1};".format(paths, default)
        else:
            self.command_prefix = "PATH={0}:{1};".format(paths, default)
        self.logger.debug("Command Prefix set to {0}".format(self.command_prefix))
        return
    
    def __getattr__(self, command):
        """
        :param:

         - `command`: The command to call.
        """
        def rpc_call(*args, **kwargs):
            return self._rpc(command, *args, **kwargs)
        return rpc_call

    def __str__(self):
        return "{0}".format(self.__class__.__name__)
# end class LocalConnection

class LocalNixConnection(LocalConnection):
    """
    A Class that uses Pexpect to get around the problem of file-buffering

    So far as I know, Pexpect only works on *nix-based systems.
    """
    def __init__(self, *args, **kwargs):
        super(LocalNixConnection, self).__init__(*args, **kwargs)
        self._logger = None
        self._operating_system = None
        return

    @property
    def operating_system(self):
        """
        :return: OperatingSystem.linux
        """
        if self._operating_system is None:
            self._operating_system = OperatingSystem.linux
        return self._operating_system

    def run(self, command, arguments):
        """
        runs the Pexpect command and puts lines of output on the Queue

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.

        :postcondition: OutputError with output and error file-like objects
        """

        if len(self.command_prefix):
            command = SPACER.format(self.command_prefix,
                                    command)
        child = pexpect.spawn(SPACER.format(command, arguments), timeout=None)
        line = None

        output_queue = Queue.Queue()
        output = StandardOutput(queue=output_queue)
        error = StringIO('')
        self.queue.put(OutputError(output, error))
        while line != EOF:
            try:
                line = child.readline()
                output_queue.put(line)
            except pexpect.TIMEOUT:
                self.logger.debug("pexpect.readline() timed out")
        output_queue.put(line)
# end class LocalNixConnection        


def yield_output(output):
    line = output.readline()
    while line:
        yield line.rstrip()
        line = output.readline()
    return

if __name__ == "__main__":
    arguments = "-l"
    lc = LocalNixConnection()
    #lc = LocalNixConnection()
    output = lc.ls(arguments='-l')
    print output.output.read()
    output = lc.ping(arguments="-c 10 192.168.0.1", timeout=1)
    for x in yield_output(output.output):
        print x
    print output.error.read()
    output = lc.iperf('-i 1 -c localhost')

    for line in yield_output( output.output):
        print line

    print output.error.read()


    output = lc.iperf('-h')
    print output.error.read()
    #for line in  output.output:
    #    print line
    print output.output.read()
    
