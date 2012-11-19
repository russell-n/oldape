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
import socket
import os


# tottest Libraries
from tottest.commons.readoutput import ValidatingOutput
from tottest.commons import enumerations


# connections
from nonlocalconnection import NonLocalConnection
from localconnection import OutputError
from sshadapter import SimpleClient

SPACER = '{0} {1}'
UNKNOWN = "Unknown command: "
EOF = ''
SPACE = ' '


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
    
    def _procedure_call(self, command, arguments="",
                        path='', timeout=10):
        """
        The reason for this is so that sub-classes can override this method
        this isn't intended to be run.
        The . notation is the expected interface.
        
        runs self._main

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.
         - `path`: An optional path to prepend to the command
         - `timeout`: readline timeout for the SSHConnection
        :return: OutputError with output and error file-like objects
        """
        return self._main(command, arguments, path, timeout)

    def _main(self, command, arguments, path, timeout):
        """
        this isn't intended to be run.
        The . notation is the expected interface.
        
        runs the SimpleClient exec_command

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.
         - `path`: An optional path to prepend to the command
         - `timeout`: readline timeout for the SSHConnection
        :return: OutputError with output and error file-like objects
        """
        self.logger.debug("command: {0}, arguments: {1}".format(command,
                                                                arguments))

        command = os.path.join(path, command)
        if len(self.command_prefix):
            command = SPACER.format(self.command_prefix,
                                    command)
        
        self.logger.debug("calling client.exec_command")
            
        stdin, stdout, stderr = self.client.exec_command(SPACER.format(command, arguments), timeout=timeout)
        
        self.logger.debug("Completed exec_command of: {0} {1}".format(command, arguments))

        return OutputError(OutputFile(stdout, self.check_errors), OutputFile(stderr, self.check_errors))

    def check_errors(self, line):
        """
        Doesn't do anything - SSHClient handles ssh errors. Overwrite in sub-classes if needed
        """
        return
    
    def __str__(self):
        return "{0} ({1}): {2}@{3} ".format(self.__class__.__name__, self.operating_system, self.username, self.hostname)
# end class SSHConnection

class OutputFile(ValidatingOutput):
    """
    A class to handle the ssh output files

    This traps socket timeouts.
    """
    def __init__(self, *args, **kwargs):
        super(OutputFile, self).__init__(*args, **kwargs)
        return

    def readline(self, timeout=10):
        """
        :param:

         - `timeout`: The length of time to wait for output

        :return: line from readline, EOF or None (in event of timeout)
        """
        if not self.empty:
            try:
                line = self.lines.readline()
                if line == EOF:
                    self.end_of_file = True
                self.validate(line)
                return line
            except socket.timeout:
                self.logger.debug("socket.timeout")
                return SPACE
        return EOF
# end class OutputFile

    
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
