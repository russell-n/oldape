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
from StringIO import StringIO

# tottest Libraries
from tottest.commons.readoutput import StandardOutput
from tottest.commons import enumerations

# connections
from threadedconnection import ThreadedConnection
from sshadapter import SimpleClient

SPACER = '{0} {1} '
UNKNOWN = "Unknown command: "
EOF = ''

OutputError = namedtuple("OutputError", 'output error')


class SSHConnection(ThreadedConnection):
    """
    An SSHConnection executes commands over an SSHConnection

    """
    def __init__(self, hostname, username,
                 password=None, port=22, timeout=5,
                 operating_system=enumerations.OperatingSystem.linux,
                 *args, **kwargs):
        """
        :param:

         - `hostname`: The IP Address or hostname
         - `username`: The login username.
         - `password`: The login password
         - `port`: The ssh port
         - `operating_system`: OperatingSystem enumeration
         - `timeout`: The login timeout
        """
        super(SSHConnection, self).__init__(*args, **kwargs)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.operating_system = operating_system
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
        Despite its name, this isn't intended to be run.
        The . notation is the expected interface.
        
        runs the SimpleClient exec_command and puts lines of output on the Queue

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.

        :postcondition: OutputError with output and error file-like objects
        """
        if len(self.command_prefix):
            command = SPACER.format(self.command_prefix,
                                    command)
        try:
            stdin, stdout, stderr = self.client.exec_command(SPACER.format(command, arguments), timeout=1)
        except:
            #self.logger.error(error)
            import sys
            self.exc_info = sys.exc_info()
            return
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
        return
    
    def __str__(self):
        return "{0} ({1}): {2}@{3} ".format(self.__class__.__name__, self.operating_system, self.username, self.hostname)
# end class SSHConnection
    
#if __name__ == "__main__":
#    arguments = "-l"
#    sc = SSHConnection("192.168.10.61", "root", 'root')
#
#    print "Testing 'ls -l'"
#    output = sc.ls(arguments='-l')
#    print output.output.read()
#
#    print "Testing ping"
#    output = sc.ping(arguments="-c 10 192.168.10.1", timeout=1)
#    for x in output.output:
#        print x
#
#    print "Reading the error"
#    # the error blocks until both standard out and standard error are finished
#    # so if you check the error first, you will probably get a socket timeout unless
#    # it goes straight to standard error (see the iperf -v example below)
#
#    print output.error.read()
#    print "Testing iperf"
#    sc.bash("PATH=$PATH:/opt/wifi")
#    output = sc.iperf(' -i 1 -c 192.168.10.51')
#    for line in output.output:
#        print line
#    print "Checking the error"
#    print "Error: " + output.error.read()
#
#    print "Checking iperf version"
#    output = sc.iperf('-v')
#
#    print output.output.read()
#    print output.error.read()    

if __name__ == "__main__":
    c = SSHConnection('igor', 'developer')
    o = c.wmic('path win32_networkadapter where netconnectionid="\'Wireless Network Connection\'" call enable')
    for index, line in enumerate(o.output):
        print index, line
