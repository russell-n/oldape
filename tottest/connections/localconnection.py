"""
a module to hold a local connection.

The LocalConnection takes the command-line command as a property and
the arguments to the command as parameters.

e.g.

    `lc = LocalConnection()`
    `output = lc.ls('-l')`
    `print output.output`

prints the output of the `ls -l` command line command

This is using subprocess so anything with lots of iperf runs the risk of
causing the output to block (i.e. it is file-buffered, not line or character buffered).

In most cases it's better to use the LocalNixConnection instead which uses Pexpect to avoid the block.
"""

#python Libraries
from subprocess import PIPE, Popen
from StringIO import StringIO
import shlex
from collections import namedtuple
import Queue
import threading

# Third-party Libraries
try:
    import pexpect
except ImportError as error:
    print error

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.commons.errors import ConnectionError
from tottest.commons.readoutput import StandardOutput
from producer import PopenProducer 

SPACER = '{0} {1} '
UNKNOWN = "Unknown command: "
EOF = ''
SPACE = " "

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

    def _local_call(self, command, arguments='', timeout=None):
        """
        This is provided so it can be overriden by subclasses.

        Otherwise it just returns _main()
        """
        return self._main(command, arguments, timeout)
    
    def _main(self, command, arguments='', block=True, timeout=None):
        """
        :param:

         - `command`: the command string to execute
         - `arguments`: The arguments for the command
         - `block`: tells the queue to block until output is available
         - `timeout`: if `block`, wait until timeout for output
        """
        try:
            self.logger.debug("Creating PopenProducer")
            process = PopenProducer(SPACE.join((self.command_prefix, command, arguments)))
            oe = OutputError(process.stdout, process.stderr)
            self.logger.debug("returning Output Error")
            
            return oe
        except OSError as error:
            self.logger.error(error)
            raise ConnectionError("Unable to execute '{0}'".format(SPACE.join((command, arguments))))
    
    def __getattr__(self, command):
        """
        :param:

         - `command`: The command to call.

        :return: The local_call method
        """
        def procedure_call(*args, **kwargs):
            return self._local_call(command, *args, **kwargs)
        return procedure_call

# end class LocalConnection

class LocalNixConnection(LocalConnection):
    """
    A Class that uses Pexpect to get around the problem of file-buffering

    So far as I know, Pexpect only works on *nix-based systems.
    """
    def __init__(self, *args, **kwargs):
        super(LocalNixConnection, self).__init__(*args, **kwargs)
        self._logger = None
        return

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
    
if __name__ == "__main__":
    arguments = "-l"
    lc = LocalConnection()
    output = lc.ls(arguments='-l')
    print output.output.read()
    output = lc.ping(arguments="-c 10 192.168.0.1", timeout=1)
    for x in output.output:
        print x
    print output.error.read()
    output = lc.iperf('-i 1 -c localhost')
    print output.output.read()

    #lc = LocalNixConnection()
    output = lc.iperf('-h')
    print output.error.read()
    #for line in  output.output:
    #    print line
    print output.output.read()
    
