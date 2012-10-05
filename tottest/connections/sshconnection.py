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
import Queue
import socket
from time import time 

# tottest Libraries
from tottest.commons.readoutput import StandardOutput
from tottest.commons import enumerations

# connections
from nonlocalconnection import NonLocalConnection
from localconnection import OutputError
from sshadapter import SimpleClient

SPACER = '{0} {1} '
UNKNOWN = "Unknown command: "
EOF = ''


class SSHConnection(NonLocalConnection):
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
        self.stop = False
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

    def abort(self):
        """
        :postcondition: self.stop is True
        """
        self.stop = True
        return
    
    def run(self, command, arguments, max_time=None):
        """
        Despite its name, this isn't intended to be run.
        The . notation is the expected interface.
        
        runs the SimpleClient exec_command and puts lines of output on the Queue

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.

        :postcondition: OutputError with output and error file-like objects
        """
        self.stop = False
        self.logger.debug("command: {0}, arguments: {1}, max_time: {2}".format(command,
                                                                               arguments,                                                                               
                                                                               max_time))
        if len(self.command_prefix):
            command = SPACER.format(self.command_prefix,
                                    command)
        try:
            self.logger.debug("Acquiring the lock to exec_command")

            with self.lock:                
                stdin, stdout, stderr = self.client.exec_command(SPACER.format(command, arguments), timeout=10)
        except:
            # the _main should check self.exc_info for an exception
            # this is to maintain a better trace (closer to the source of the exception
            import sys
            self.exc_info = sys.exc_info()
            return
        self.logger.debug("Completed exec_command of: {0} {1}".format(command, arguments))
        line = None

        #output = StandardOutput(stdout)
        self.queue.put(OutputError(stdout, stderr))

        #if max_time is not None:
        #    now = time
        #    abort_time = now() + max_time
        #else:
        #    now = lambda:0
        #    abort_time = 1
        #
        #self.logger.debug("max_time: {0}, abort_time: {1}".format(max_time, abort_time))
        #while line != EOF and not self.stop:
        #    try:
        #        line = stdout.readline()
        #        output_queue.put(line)
        #    except socket.timeout:
        #        self.logger.debug("{0} {1}: socket.timeout: stdout.readline() timed out".format(command, arguments))
        #        self.logger.debug("{0} seconds out of {1} max allowed seconds".format(abort_time-now(), max_time))
        #    if now() > abort_time:
        #        self.logger.error("Aborting, {0} seconds exceeded.".format(max_time))
        #        line = EOF
        #output_queue.put(line)
        #if line != EOF:
        #    output_queue.put(EOF)
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
