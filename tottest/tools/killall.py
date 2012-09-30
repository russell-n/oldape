"""
A module to kill processes
"""

#python
import re

# tottest
from tottest.baseclass import BaseClass
from tottest.tools import sleep
from tottest.commons import enumerations, expressions, errors
from tottest.parsers.oatbran import NAMED, STRING_START,SPACES, INTEGER

CYGWIN = STRING_START + SPACES + NAMED(n=expressions.PID_NAME,e=INTEGER)

operating_systems = enumerations.OperatingSystem

class KillAllError(errors.CommandError):
    """
    A KillAllError is raised if the kill didn't succeed.
    """

class KillAll(BaseClass):
    """
    A killall kills processes. The default operating system is linux
    """
    def __init__(self, name=None, sleep=5):
        """
        :param:

         - `name`: The name of a process to kill
         - `sleep`: The number of seconds to wait for a process to die.
        """
        super(BaseClass, self).__init__()
        self._logger = None
        self.name = name
        self._expression = None
        self._arguments = None
        self.time_to_sleep = sleep
        self._sleep = None
        return

    @property
    def operating_system(self):
        """
        :precondition: self.connection has the connection to the device
        
        :return: The operating system that issues the commands.
        """
        if self._operating_system is None:
            self._operating_system = self.connection.operating_system
            if self._operating_system is None:
                self._operating_system = operating_systems.linux
            self.logger.debug("KillAll Operating sytem: {0}".format(self._operating_system))
        return self._operating_system

    @property
    def expression(self):
        """
        :return: The regular expression for the ps command
        """
        if self.operating_system == operating_systems.android:
            self.logger.debug("Using Android Expression")
            return re.compile(expressions.PS_ANDROID)
        if self.operating_system == operating_systems.windows:
            self.logger.debug("Using Cygwin Expression")
            return re.compile(CYGWIN)

        self.logger.debug("Using linux expression")
        return re.compile(expressions.PSE_LINUX)

    @property
    def arguments(self):
        """
        :return: The arguments to the `ps` call        
        """
        if self.operating_system == operating_systems.android:
            return ''
        return "-e"

    @property
    def sleep(self):
        """
        :return: A sleep timer
        """
        if self._sleep is None:
            self._sleep = sleep.Sleep().run
        return self._sleep
    
    def run(self, connection, name=None, time_to_sleep=None):
        """
        :param:

         - `connection`: the connection to the device
         - `name`: The process to kill

        :raise: KillAllError if the process is still alive at the end
        """
        self.connection = connection
        if name is None:
            name = self.name
        
        if time_to_sleep is None:
            time_to_sleep = self.time_to_sleep

        self.logger.debug("name = " + name)
        output, error = self.connection.ps(self.arguments)
        
        for line in output:
            # line is the next line returned from stdout
            if name in line:
                self.logger.debug(line)
            match = self.expression.search(line)
            if match and match.group(expressions.PROCESS_NAME) == name:
                self.logger.debug("matched: " + line)
                self.logger.debug("killing: " + match.group(expressions.PID_NAME))
                command = " -9 " + match.group(expressions.PID_NAME)
                self.logger.debug("kill " + command)
                k_output, k_error = self.connection.kill(command)
                for k_line in k_error:
                    self.logger.error(k_line)
        err = error.read()
        if len(err):
            self.logger.error(err)
        self.sleep(time_to_sleep)

        # double-check to see if the process is dead
        output, error = self.connection.ps(self.arguments)
        for process in output:
            if name in line:
                self.logger.error(line)

            match = self.expression.search(process)
            if match and match.group(expressions.PROCESS_NAME) == name:
                err = error.read()
                if len(err):
                    self.logger.error(err)
                raise KillAllError("Unable to kill {0}".format(name))
        err = error.read()
        if len(err):
            self.logger.error(err)
        return

    def __call__(self, connection, name=None, time_to_sleep=None):
        """
        This is an alias to run to match the newer-style
        :param:

         - `connection`: connection to the device
        """
        self.run(name, time_to_sleep)
        return
    
    def __str__(self):
        return "{0} ({2}):{1}".format(self.__class__.__name__, self.name, self.connection)
# class KillAll
