"""
A module to kill processes
"""

#python
import re

# tottest
from tottest.baseclass import BaseClass
from tottest.tools import sleep
from tottest.commons import enumerations, expressions, errors

operating_systems = enumerations.OperatingSystem

class KillAllError(errors.CommandError):
    """
    A KillAllError is raised if the kill didn't succeed.
    """

class KillAll(BaseClass):
    """
    A killall kills processes. The default operating system is linux
    """
    def __init__(self, connection, name=None, operating_system=None, sleep=5):
        """
        :param:

         - `connection`: a device connection
         - `name`: The name of a process to kill
         - `operating_system`: The OS whose `ps` will be used
         - `sleep`: The number of seconds to wait for a process to die.
        """
        super(BaseClass, self).__init__()
        self._logger = None
        self.connection = connection
        self.name = name
        self._operating_system = operating_system
        self._expression = None
        self._arguments = None
        self.time_to_sleep = sleep
        self._sleep = None
        return

    @property
    def operating_system(self):
        """
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
        if self._expression is None:
            if self.operating_system == operating_systems.android:
                self.logger.debug("Using Android Expression")
                self._expression = re.compile(expressions.PS_ANDROID)
            else:
                self.logger.debug("Using linux expression")
                self._expression = re.compile(expressions.PSE_LINUX)

        return self._expression

    @property
    def arguments(self):
        """
        :return: The arguments to the `ps` call        
        """
        if self._arguments is None:
            if self.operating_system == operating_systems.android:
                self._arguments = ''
            else:
                self._arguments = "-e"
            
        return self._arguments

    @property
    def sleep(self):
        """
        :return: A sleep timer
        """
        if self._sleep is None:
            self._sleep = sleep.Sleep().run
        return self._sleep
    
    def run(self, name=None, time_to_sleep=None):
        """
        :name: The process to kill

        :raise: KillAllError if the process is still alive at the end
        """
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
                for k_line in k_output:
                    self.logger.debug(k_line)
                for k_line in k_error:
                    self.logger.error(k_line)
        err = error.read()
        if len(err):
            self.logger.error(err)
        self.sleep(time_to_sleep)
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

    def __call__(self, name=None, time_to_sleep=None):
        self.run(name, time_to_sleep)
    
    
    def __str__(self):
        return "{0} ({2}):{1}".format(self.__class__.__name__, self.name, self.connection)
# class KillAll
