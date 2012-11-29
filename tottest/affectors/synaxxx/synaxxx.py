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

NEWLINE = "\n\r"
INVALID = "Invalid command"
EOF = ''
SWITCH_ON = 'pset {0} 1' + NEWLINE
ALL_OFF = 'ps 0' + NEWLINE
ALL_ON = 'ps 1' + NEWLINE
SHOW_STATUSES = 'pshow' + NEWLINE

ON = 'ON'
OFF = "OFF"

ONE_OR_MORE = r'+'
DIGIT = r'\d'
INTEGER = DIGIT + ONE_OR_MORE
STATE = '(?P<state>ON|OFF)'
SWITCH = '(?P<switch>{0})'.format(INTEGER)
ANYTHING = '.'
EVERYTHING = ANYTHING + ONE_OR_MORE
state_expression = re.compile(SWITCH + EVERYTHING + STATE)

class SynaxxxError(Exception):
    """
    An error to raise if a command doesn't execute properly.
    """
# end class SynaxxxError
    

class Synaxxx(object):
    """
    A class to control the Synaxxx
    """
    def __init__(self, host, port=23, timeout=1, sleep=0, debug=False):
        """
        :param:

         - `host`: the hostname or IP of the target
         - `port`: the port number for the telnet service
         - `timeout`: the login and read timeout in seconds
         - `sleep`: time to sleep between changing the state of the same switch
         - `debug`: If true, show synaccess output
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sleep = sleep
        self.debug = debug
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
        :yield: line of output
        """
        self.client.read_very_eager()
        self.client.write(NEWLINE)
        self.client.write(command + NEWLINE)
        for line in self.lines():            
            self.validate(line, command)
            yield line
        return 
    
    def lines(self):
        """
        :yield: each line of output
        """
        line = None
        while line != EOF:
            line = self.client.read_until(NEWLINE, 1)
            if self.debug:
                print line
            yield line
        return

    def validate(self, line, command):
        """
        Checks the line for errors.
        """
        if INVALID in line:
            raise SynaxxxError("Error executing: '{0}'".format(command.strip()))
        return
    
    def all_off(self):
        """
        :postcondition: all outlets turned off
        """
        for line in self.exec_command(ALL_OFF):
            pass
        return

    def all_on(self):
        """
        :postcondition: all outlets turned off
        """
        for line in self.exec_command(ALL_ON):
            pass
        return

    def turn_on(self, switch):
        """
        :param:

         - `switch`: a switch identifier
        """
        for line in self.exec_command(SWITCH_ON.format(switch)):
            pass
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
            if switch not in self.status:
                #raise SynaxxxError("Invalid Switch: '{0}'".format(switch))
                print "Invalid Switch: '{0}'".format(switch)
                continue
            self.turn_on(switch)

        statuses = self.status
        for switch in switches:
            try:
                assert statuses[switch] == ON
            except (AssertionError, KeyError):
                #raise SynaxxxError("Unable to turn on switch '{0}'".format(switch))
                print "Unable to turn on switch '{0}'".format(switch)
        for switch in [switch for switch in statuses if switch not in switches]:
            try:
                assert statuses[switch] == OFF
            except (AssertionError, KeyError):
                #raise SynaxxxError("Unable to turn off switch '{0}'".format(switch))
                print "Unable to turn off switch '{0}'".format(switch)
        self.show_status()
        return

    def show_status(self):
        """
        print switch states to stdout
        """
        for switch in sorted(self.status):
            print switch, self.status[switch]
        return

    def close(self):
        """
        :postcondition: connection closed, client deleted
        """
        self.client.close()
        self._client = None
        return
# end class Synaxxx
