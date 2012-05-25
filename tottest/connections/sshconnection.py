"""
a module to hold an SSH connection.

The SSHConnection takes the command-line command as a property and
the arguments to the command as parameters.

e.g.

    `sc = SSHConnection()`
    `output = sc.ls('-l')`
    `print output.output`

prints the output of the `ls -l` command line command

"""

#python Libraries
from collections import namedtuple
import Queue
import socket

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.commons.errors import ConnectionError
from tottest.commons.readoutput import StandardOutput

# connections
from localconnection import LocalConnection
from sshadapter import SimpleClient

SPACER = '{0} {1} '
UNKNOWN = "Unknown command: "
EOF = ''

OutputError = namedtuple("OutputError", 'output error')


class SSHConnection(LocalConnection):
    """
    An SSHConnection executes commands over an SSHConnection

    """
    def __init__(self, hostname, username,
                 password=None, port=22, timeout=5,
                 *args, **kwargs):
        """
        :param:

         - `hostname`: The IP Address or hostname
         - `username`: The login username.
         - `password`: The login password
         - `port`: The ssh port
         - `timeout`: The login timeout
        """
        super(SSHConnection, self).__init__(*args, **kwargs)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self._logger = None
        self._client = None
        return

    @property
    def client(self):
        """
        :return: SimpleClient for the SSHConnection
        """
        if self._client is None:
            self._client = SimpleClient(hostname=self.hostname, username=self.username,
                                        password=self.password, port=self.port,
                                        timeout=self.timeout)
        return self._client
    
    def run(self, command, arguments):
        """
        runs the SimpleClient exec_command and puts lines of output on the Queue

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.

        :postcondition: OutputError with output and error file-like objects
        """
        if len(self.command_prefix):
            command = SPACER.format(self.command_prefix,
                                    command)
        stdin, stdout, stderr = self.client.exec_command(SPACER.format(command, arguments), timeout=1)
        line = None

        output_queue = Queue.Queue()
        output = StandardOutput(queue=output_queue)
        self.queue.put(OutputError(output, stderr))
        while line != EOF:
            try:
                line = stdout.readline()
                output_queue.put(line)
            except socket.timeout:
                self.logger.debug("stdout.readline() timed out")
        output_queue.put(line)
# end class LocalNixConnection        
    
if __name__ == "__main__":
    arguments = "-l"
    sc = SSHConnection("localhost", "allion")
    output = sc.ls(arguments='-l')
    print output.output.read()
    output = sc.ping(arguments="-c 10 192.168.10.1", timeout=1)
    for x in output.output:
        print x
    print output.error.read()
    output = sc.iperf('-i 1 -c localhost')
    print output.output.read()
    if len(output.error.buf):
        print "Error: " + output.error.read()

    #lc = LocalNixConnection()
    output = sc.iperf('-h')
    print output.error.read()
    #for line in  output.output:
    #    print line
    print output.output.read()
    
