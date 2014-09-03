"""
This is a module to hold a telnet adapter.
"""

# python Libraries
import telnetlib

# apetools libraries

from apetools.baseclass import BaseClass

NEWLINE = '\n'
EOF = EMPTY_STRING = ''


class TelnetAdapter(BaseClass):
    """
    A TelnetAdapter Adapts the telnetlib.Telnet to this libraries interfaces.
    """
    def __init__(self, host, prompt="#", login='root', password=None, port=23, timeout=2, end_of_line='\r\n',
                 login_prompt="login:"):
        """
        :param:

         - `host`: The address of the telnet server
         - `prompt`: The prompt used on the device
         - `port`: The port of the telnet server
         - `login`: The login (if needed)
         - `timeout`: The timeout for blocking methods
         - `end_of_line`: The end of line string used by the device.
         - `login_prompt`: The prompt to look for when starting a connection.
         - `password`: if given tries to login
        """
        super(TelnetAdapter, self).__init__()
        self.host = host
        self.prompt = prompt
        self.login = login
        self.port = port
        self.timeout = timeout
        self.end_of_line = end_of_line
        self._client = None
        self.login_prompt = login_prompt
        return

    @property
    def client(self):
        """
        Tries to login before returning.

        :rtype: telnetlib.Telnet
        :return: The telnet client
        """
        if self._client is None:
            self._client = telnetlib.Telnet(host=self.host, port=self.port,timeout=self.timeout)
            possibilities = [self.prompt, self.login_prompt]
            output = self._client.expect(possibilities, timeout=self.timeout)
            if output[0] == 1:
                self._client.write(self.login + NEWLINE)
        return self._client

    def exec_command(self, command, timeout=10):
        """
        The main interface.

        Since I'm hiding the client from users, this will do a read_very_eager before continuing.
        The read is intended to try and flush the output

        :param:

         - `command`: The command to execute on the device
         - `timeout`: The readline timeout

        :return: TelnetOutput with the this object's as client
        """
        self.client.timeout = timeout
        self.logger.debug("In queue: " + self.client.read_very_eager())
        self.logger.debug("Sending the command: " + command)
        self.writeline(command)
        return TelnetOutput(client=self.client, prompt=self.prompt,
                            timeout=self.timeout, end_of_line=self.end_of_line)
                           
    
    def writeline(self, message=""):
        """
        :param:

         - `message`: A message to send to the device.
        """
        self.client.write(message.rstrip(NEWLINE) + NEWLINE)
        return
    
    def __del__(self):
        self.client.close()
        return
# end class TelnetAdapter

MATCH_INDEX = 0
MATCHING_STRING = 2

class TelnetOutput(BaseClass):
    """
    The TelnetOutput converts the telnet output to a file-like object
    """
    def __init__(self, client, prompt="#", end_of_line='\r\n',timeout=10):
        """
        :param:

         - `client` : a connected telnet client
         - `prompt`: The current prompt on the client
         - `end_of_line`: Then end of line character
         - `timeout`: The readline timeout
        """
        super(TelnetOutput, self).__init__()
        self.client = client
        self.prompt = prompt
        self.end_of_line = end_of_line
        self.timeout = timeout
        self.endings = [end_of_line, prompt]
        self.line_ending_index = 0
        self.finished = False
        return

    def readline(self, timeout=None):
        """
        :param:

         - `timeout`: The readline timeout
         
        :return: The next line of text
        """
        if timeout is None:
            timeout = self.timeout

        output = self.client.expect(self.endings, timeout)
        if self.finished:
            return EOF
        elif output[MATCH_INDEX] == self.line_ending_index:
            return output[MATCHING_STRING]
        else:
            # matched the prompt, this output is finished
            self.logger.debug("Stopping on : " + output[MATCHING_STRING])
            self.finished = True
        return EOF

    def next(self):
        """
        :yield: the next line
        """
        while not self.finished:
            yield self.readline()
        return

    def readlines(self):
        """
        :return: A list of lines
        """
        lines = []
        line = None
        while line != EOF:
            line = self.readline()
            lines.append(line)
        return lines

    def read(self):
        """
        :return: String of output
        
        """
        return EMPTY_STRING.join(self.readlines())

    def __iter__(self):
        return self.next()
# end class TelnetOutput

if __name__ == "__main__":
    ta = TelnetAdapter(host="192.168.10.172")
    for line in ta.exec_command("iperf -c 192.168.10.51 -i 1"):
        print line
