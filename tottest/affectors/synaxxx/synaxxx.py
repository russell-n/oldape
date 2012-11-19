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
import time
import re

# tottest modules
from tottest.baseclass import BaseClass
from tottest.parsers import oatbran

NEWLINE = "\n\r"
INVALID = "Invalid command"
EOF = ''
SWITCH_ON = 'pset {0} 1' + NEWLINE
ALL_OFF = 'ps 0' + NEWLINE
SHOW_STATUSES = 'pshow' + NEWLINE
ON = 'ON'
OFF = "OFF"
STATE = '(?P<state>ON|OFF)'
SWITCH = '(?P<switch>{0})'.format(oatbran.INTEGER)
state_expression = re.compile(SWITCH + oatbran.EVERYTHING + STATE)

class Synaxxx(BaseClass):
    """
    A class to control the Synaxxx
    """
    def __init__(self, host, port=23, timeout=1, sleep=5):
        """
        :param:

         - `host`: the hostname or IP of the target
         - `port`: the port number for the telnet service
         - `timeout`: the login and read timeout in seconds
         - `sleep`: time to sleep between changing the state of the same switch
        """
        super(Synaxxx, self).__init__()
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sleep = sleep
        self._client = None
        self._status = None

    @property
    def client(self):
        """
        :return: the telnetlib client
        """
        if self._client is None:
            self._client = telnetlib.Telnet(self.host, self.port, self.timeout)
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
                statuses[states['switch']] = states['state']
        return statuses

    def exec_command(self, command):
        """
        :param:

         - `command`: a string to send to the device

        :postcondition: command string sent to the device
        :yield: the lines of output
        """
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
        """
        if INVALID in line:
            print "error: " + line
        return
    
    def all_off(self):
        """
        :postcondition: all outlets turned off
        """
        for line in self.exec_command("ps 0"):
            self.validate(line)
        return

    def all_on(self):
        """
        :postcondition: all outlets turned off
        """
        for line in self.exec_command("ps 1"):
            self.validate(line)
        return
    
    def __call__(self, switches=None):
        """
        :param:

         - `switches`: a list of switches (integers)

        :postcondition: switches in list on, all others off
        """
        self.all_off()
        time.sleep(self.sleep)
        if switches is None:
            return
        for switch in switches:
            for line in self.exec_command("pset {0} 1".format(switch)):
                self.validate(line)
                print line
        statuses = self.status
        for switch in switches:
            assert statuses[switch] == ON
        for switch in [switch for switch in statuses if switch not in switches]:
            assert statuses[switch] == OFF
        return
# end class Synaxxx
