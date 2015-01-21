
#python Libraries
from collections import namedtuple
from StringIO import StringIO
import os

# apetools Libraries
from localconnection import OutputError
from sshconnection import OutputFile

# connections
from localconnection import LocalConnection
from serialadapter import SerialAdapter


SPACER = '{0} {1} '
UNKNOWN = "command not found "
EOF = ''


class SerialConnection(LocalConnection):
    """
    A SerialConnection executes commands over a serial connections

    """
    def __init__(self, port, baudrate, timeout=10,
                 prompt=None, prompt_length=10,                 
                 *args, **kwargs):
        """
        :param:

         - `port`: The Serial port name
         - `baudrate`: The baudrate of the port
         - `prompt`: an alternative prompt to use (default is random)
         - `prompt_length`: The length to make the random prompt
         - `timeout`: The readline timeout
        """
        super(SerialConnection, self).__init__(*args, **kwargs)
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._prompt = None
        self.prompt = prompt
        self.prompt_length = prompt_length
        self._client = None
        return

    @property
    def client(self):
        """
        :return: SerialAdapter for the Serial Connection
        """
        if self._client is None:
            self._client = SerialAdapter(port=self.port, baudrate=self.baudrate,
                                        timeout=self.timeout)
        return self._client

    def set_timeout(self, new_timeout):
        """
        Some of the configuration commands for devices take a long time.

        This sets the client's timeout to whatever you want.

        :param:

         - `new_timeout`: A timeout value in seconds for the Device
        """
        self.client.timeout = new_timeout
        return
    
    def _procedure_call(self, command, arguments="",
                        path="", timeout=10):
        """
        Despite its name, this isn't intended to be run.
        The . notation is the expected interface.
        
        runs the SimpleClient exec_command and puts lines of output on the Queue

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.
         - `path`: path to prepend to the command

        :postcondition: OutputError with output and error file-like objects
        """
        command = os.path(path, command)
        if len(self.command_prefix):
            command = SPACER.format(self.command_prefix,
                                    command)
        stdout = self.client.exec_command(SPACER.format(command, arguments),
                                          timeout=timeout)
        self.logger.debug("Completed 'client.exec_command({0})'".format(command))
        stderr = StringIO("")
        return OutputError(OutputFile(stdout), stderr)

# end class SerialConnection        


if __name__ == "__main__":
    arguments = "-l"
    sc = SerialConnection("/dev/ttyUSB0", 115200)

    #import curses.ascii
    #sc.client.writeline(curses.ascii.ctrl("c"))
    sc.set_timeout(1)
    print "Testing 'ls -l'"
    output = sc.ls(arguments='-l /opt/wifi/atheros')
    print output.output.read()

    # semco
    print "sourcing the setup"
    sc.client.writeline("source setup.sh")
    sc.set_timeout(5)
    output = sc.echo("$PATH")
    print "Echoing the path"
    print output.output.read()
    output = sc.bash("/opt/wifi/atheros/wifi.sh init")
    print output.output.read()
    output = sc.bash("/opt/wifi/atheros/wifi.sh connect wndr3700 testlabs")
    print output.output.read()
    print sc.iwconfig().output.read()
    print "Testing ping"
    output = sc.ping(arguments="-c 10 192.168.10.1", timeout=1)
    for x in output.output:
        print x

    print "Reading the error"
    # the error blocks until both standard out and standard error are finished
    # so if you check the error first, you will probably get a socket timeout unless
    # it goes straight to standard error (see the iperf -v example below)

    print output.error.read()
    print "Testing iperf"
    output = sc.iperf('-i 1 -c 192.168.20.51')
    for line in output.output:
        print line

    print "Checking iperf version"
    output = sc.iperf('-v')

    print output.output.read()
    print sc.reboot().output.read()
