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
import time

#apetools library
from apetools.baseclass import BaseClass
from apetools.tools.sleep import Sleep
from apetools.commons.errors import CommandError

NEWLINE = "\r"
INVALID = "Invalid command"
EOF = ''
SWITCH_ON = 'pset {0} 1'
ALL_OFF = 'ps 0'
ALL_ON = 'ps 1'
SHOW_STATUSES = 'pshow'

ON = 'ON'
OFF = "OFF"

ZERO_OR_MORE = r"*"
ONE_OR_MORE = r'+'
DIGIT = r'\d'
INTEGER = DIGIT + ONE_OR_MORE
STATE = '(?P<state>ON|OFF)'
SWITCH = '(?P<switch>{0})'.format(INTEGER)
ANYTHING = '.'
EVERYTHING = ANYTHING + ONE_OR_MORE
SEPARATOR = r'\|'
SPACE = r'\s'
SPACES = SPACE + ZERO_OR_MORE
state_expression = re.compile(SWITCH + SPACES + SEPARATOR + SPACES + "Outlet" +
                              INTEGER + SPACES + SEPARATOR + SPACES + STATE)


class SynaxxxError(CommandError):
    """
    An error to raise if a command doesn't execute properly.
    """
# end class SynaxxxError


class Synaxxx(BaseClass):
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
        super(Synaxxx, self).__init__()
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sleep = sleep
        self.debug = debug
        self._client = None
        self._status = None
        self._sleeper = None
        return

    @property
    def sleeper(self):
        """
        :return: a sleeper
        """
        if self._sleeper is None:
            self._sleeper = Sleep(self.sleep)
        return self._sleeper

    @property
    def client(self):
        """
        :return: the telnetlib client
        """
        if self._client is None:
            message = "Opening telnet connection: {0}@{1}"
            self.logger.debug(message.format(self.host,
                                             self.port))
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

    def exec_command(self, command, attempts=2):
        """
        :param:

         - `command`: a string to send to the device
         - `attempts`: number of times to try (the server tends to die)

        :postcondition: command string sent to the device
        :yield: line of output
        """
        for attempt in range(attempts):
            try:
                self.client.read_very_eager()
                self.client.write(NEWLINE)
                self.client.write(command + NEWLINE)
                for line in self.lines():
                    self.validate(line, command)
                    yield line
            except (socket.timeout, socket.error) as error:
                self.logger.error("Telnet Error: {0}".format(error))
                self.close()
                if attempt == attempts - 1:
                    message = "Error with: ip: {0} port: {1}"
                    raise SynaxxxError(message.format(self.host,
                                                      self.port))
        return

    def lines(self, timeout=120):
        """
        :param:

         - `timeout`: maximum time to yield lines

        :yield: each line of output
        """
        line = None
        end_time = time.time() + timeout

        while line != EOF:
            line = self.client.read_until(NEWLINE, 1)
            self.logger.debug(line)
            yield line
            if time.time() > end_time:
                raise SynaxxxError("time exceeded {0} seconds".format(timeout))
        return

    def validate(self, line, command):
        """
        Checks the line for errors.
        """
        if INVALID in line:
            message = "Error executing: '{0}'"
            raise SynaxxxError(message.format(command.strip()))
        return

    def all_off(self):
        """
        :postcondition: all outlets turned off
        """
        self.logger.info("Turning all switches off")
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

        :postcondition: switches in list on, all others off, self.close called
        """
        self.all_off()

        self.sleeper()
        if switches is None:
            return

        for switch in switches:
            self.logger.info("Turning on switch {0}".format(switch))
            if switch not in self.status:
                self.increment_sleep()
                raise SynaxxxError("Invalid Switch: '{0}'".format(switch))
            self.turn_on(switch)

        self.logger.info("Validating switch states")
        statuses = self.status
        for switch in switches:
            try:
                assert statuses[switch] == ON
            except (AssertionError, KeyError):
                self.increment_sleep()
                SynaxxxError("Unable to turn on switch '{0}'".format(switch))
        for switch in [switch for switch in statuses
                       if switch not in switches]:
            try:
                assert statuses[switch] == OFF
            except (AssertionError, KeyError):
                self.increment_sleep()
                message = "Unable to turn off switch '{0}'"
                raise SynaxxxError(message.format(switch))
        self.show_status()
        self.close()
        return

    def increment_sleep(self):
        """
        :postcondition: sleep increased by one second
        """
        self.sleep += 1
        self.sleeper.sleep_time = self.sleep
        self.logger.debug("Sleep time increased to {0}".format(self.sleep))
        return

    def show_status(self):
        """
        print switch states to stdout
        """
        for switch in sorted(self.status):
            self.logger.info("{0} {1}".format(switch, self.status[switch]))
        return

    def close(self):
        """
        :postcondition: connection closed, client deleted
        """
        try:
            self.client.close()
        except socket.error as error:
            self.logger.debug(error)
        self._client = None
        return
# end class Synaxxx
