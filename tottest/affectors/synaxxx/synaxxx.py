# Copyright 2012 Russell Nakamura
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
A module to adapt the Synaccess network controller.
"""

#python standard library
import telnetlib
import re
import socket
from types import ListType

# tottest modules
from tottest.baseclass import BaseClass
from tottest.parsers import oatbran
from tottest.commons.errors import CommandError, ConnectionError
from tottest.tools.sleep import Sleep

NEWLINE = "\n\r"
INVALID = "Invalid command"
EOF = ''
SWITCH_ON = 'pset {0} 1' 
ALL_OFF = 'ps 0' 
ALL_ON = 'ps 1' 
SHOW_STATUSES = 'pshow' 
ON = 'ON'
OFF = "OFF"
STATE_NAME = 'state'
SWITCH_NAME = 'switch'
STATE = oatbran.NAMED(n=STATE_NAME,e=ON + oatbran.OR + OFF)
SWITCH = oatbran.NAMED(n=SWITCH_NAME, e=oatbran.INTEGER)
state_expression = re.compile(SWITCH + oatbran.EVERYTHING + STATE)

class SynaxxxError(CommandError):
    """
    An error to raise in the event there is an invalid command
    """
# end class SynaxxxError

class SynaxxxConnectionError(ConnectionError):
    """
    An error to raise if the socket times out
    """
# end class SynaxxxConnectionError

    
class Synaxxx(BaseClass):
    """
    A class to control the Synaxxx
    """
    def __init__(self, hostname, port=23, timeout=5, wait_time=5):
        """
        :param:

         - `hostname`: the hostname or IP of the target
         - `port`: the port number for the telnet service
         - `timeout`: the login and read timeout in seconds
         - `wait_time`: time to sleep between changing the state of the same switch
        """
        super(Synaxxx, self).__init__()
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.wait_time = wait_time
        self.last_command = None
        self._client = None
        self._status = None
        self._sleep = None
        return

    @property
    def sleep(self):
        """
        :return: A sleep object
        """
        if self._sleep is None:
            self._sleep = Sleep(self.wait_time)
        return self._sleep
    
    @property
    def client(self):
        """
        :return: the telnetlib client
        """
        if self._client is None:
            try:
                self._client = telnetlib.Telnet(self.hostname, self.port, self.timeout)
            except socket.error:
                raise SynaxxxConnectionError("Synaxxx Connection to: {0}:{1} failed (is it online?)".format(self.hostname, self.port))
        return self._client

    @property
    def status(self):
        """
        :return: dict of <switch id>:<state>
        """
        statuses = {}
        for line in self.exec_command(SHOW_STATUSES):
            match = state_expression.search(line)
            if match:
                states = match.groupdict()
                statuses[states[SWITCH_NAME]] = states[STATE_NAME]
        return statuses

    def exec_command(self, command):
        """
        :param:

         - `command`: a string to send to the device

        :postcondition: command string sent to the device
        :yield: the lines of output
        """
        self.last_command = command
        self.client.write(NEWLINE)
        self.client.read_very_eager()
        self.client.write(command + NEWLINE)
        for line in self.lines():
            yield line
        return 
    
    def lines(self):
        """
        :yield: each line of output
        """
        line = None
        while line != EOF:
            line = self.client.read_until(NEWLINE, 1)            
            yield line
        return

    def validate(self, line):
        """
        Checks the line for errors.

        :raise: SynaxxxError if an error is detected
        """
        self.logger.debug(line)
        if INVALID in line:
            raise SynaxxxError("error: {0} {1}".format(self.last_command,
                                                       line))
        return
    
    def all_off(self):
        """
        :postcondition: all outlets turned off
        """
        for line in self.exec_command(ALL_OFF):
            self.validate(line)
        return

    def all_on(self):
        """
        :postcondition: all outlets turned off
        """
        for line in self.exec_command(ALL_ON):
            self.validate(line)
        return
    
    def __call__(self, switches=None):
        """
        :param:

         - `switches`: a list of switches (integers)

        :postcondition: switches in list on, all others off
        """
        self.logger.info("Turning all power-switches off")
        self.all_off()
        self.sleep()
        if type(switches) is not ListType and switches is not None:
            switches = [switches]
        if switches is None:
            switches = []
        for switch in switches:
            self.logger.info("Turning on switch {0}".format(switch))
            for line in self.exec_command(SWITCH_ON.format(switch)):
                self.validate(line)
        statuses = self.status
        for switch in switches:
            if not statuses[switch] == ON:
                raise SynaxxxError("Switch {0} not successfully turned on.".format(switch))
        for switch in [switch for switch in statuses if switch not in switches]:
            if not statuses[switch] == OFF:
                raise SynaxxxError("Unable to turn off switch {0}.".format(switch))
        return
# end class Synaxxx
