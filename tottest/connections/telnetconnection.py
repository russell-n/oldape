"""
A module to hold an Telnet connection.

The TelnetConnection takes the command-line command as a property and
the arguments to the command as parameters.

e.g.

    `sc = TelnetConnection()`
    `output = sc.ls('-l')`
    `print output.output`

prints the output of the `ls -l` command line command

"""

#python Libraries
from collections import namedtuple
import Queue
from StringIO import StringIO

# tottest Libraries
from tottest.commons.readoutput import StandardOutput
#commands
from tottest.commands import changeprompt

# connections
from nonlocalconnection import NonLocalConnection
from telnetadapter import TelnetAdapter

SPACER = '{0} {1} '
UNKNOWN = "Unknown command: "
EOF = ''

OutputError = namedtuple("OutputError", 'output error')


class TelnetConnection(NonLocalConnection):
    """
    A TelnetConnection executes commands over a Telnet Connection

    """
    def __init__(self, hostname, port=23, login="root", prompt="#", timeout=2, end_of_line='\r\n',
                 *args, **kwargs):
        """
        :param:

         - `hostname`: The IP Address or hostname
         - `port`: The telnet port 
         - `login`: The login name
         - `prompt`: The prompt to expect
         - `timeout`: The readline timeout
         - `end_of_line`: The string indicating the end of a line.
        """
        super(TelnetConnection, self).__init__(*args, **kwargs)
        self.hostname = hostname
        self.port = port
        self.login = login
        self.prompt = prompt
        self.timeout = timeout
        self.end_of_line = end_of_line
        self._logger = None
        self._client = None
        return

    @property
    def client(self):
        """
        :return: TelnetAdapter for the telnet connection
        """
        if self._client is None:
            self._client = TelnetAdapter(host=self.hostname, 
                                         login=self.login, port=self.port,
                                         timeout=self.timeout,
                                         end_of_line=self.end_of_line,
                                         prompt=self.prompt)
            changer = changeprompt.ChangePrompt(adapter=self._client)
            self.logger.debug(changer.run())
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
        stdout = self.client.exec_command(SPACER.format(command, arguments), timeout=1)
        line = None

        output_queue = Queue.Queue()
        output = StandardOutput(queue=output_queue)
        stderr = StringIO("")
        self.queue.put(OutputError(output, stderr))
        while line != EOF:
            line = stdout.readline()
            output_queue.put(line)
        output_queue.put(line)
# end class TelnetConnection
    
if __name__ == "__main__":
    import curses.ascii
    arguments = "-l"
    sc = TelnetConnection("192.168.10.172")
    sc.client.writeline(curses.ascii.crtl("c"))
    print "Testing 'ls -l'"
    output = sc.ls(arguments='-l')
    for x in output.output:
        print x

    from time import sleep
    sleep(0.1)
    print "Testing ping"
    output = sc.ping(arguments="-c 10 192.168.10.1", timeout=1)
    for x in output.output:
        print x

    sleep(0.1)
    print "Testing iperf"
    output = sc.iperf('-i 1 -c 192.168.10.51')
    for line in output.output:
        print line

    sleep(0.1)
    print "Checking iperf version"
    output = sc.iperf('-v')

    print output.output.read()
    print output.error.read()    
