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
    def __init__(self, connection, name=None, operating_system=None):
        """
        :param:

         - `connection`: a device connection
         - `name`: The name of a process to kill
         - `operating_system`: The OS whose `ps` will be used
        """
        super(BaseClass, self).__init__()
        self.connection = connection
        self.name = name
        self._operating_system = operating_system
        self._expression = None
        self._arguments = None
        self._sleep = None
        return

    @property
    def operating_system(self):
        """
        :return: The operating system that issues the commands.
        """
        if self._operating_system is None:
            self._operating_system = operating_systems.linux
        return self._operating_system

    @property
    def expression(self):
        """
        :return: The regular expression for the ps command
        """
        if self._expression is None:
            if self.operating_system == operating_systems.linux:
                self._expression = re.compile(expressions.PSE_LINUX)
        return self._expression

    @property
    def arguments(self):
        """
        :return: The arguments to the `ps` call        
        """
        if self._arguments is None:
            if self.operating_system == operating_systems.linux:
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
    
    def run(self, name=None):
        """
        :name: The process to kill

        :raise: KillAllError if the process is still alive at the end
        """
        if name is None:
            name = self.name
        for process in self.connection.ps(self.arguments):
            match = self.expression.search(process)
            if match and match.group(expressions.PROCESS_NAME) == name:
                self.connection.kill(match.group(expressions.PID_NAME))
        self.sleep()
        for process in self.connection.ps(self.arguments):
            match = self.expression.search(process)
            if match and match.group(expressions.PROCESS_NAME) == name:
                raise KillAllError("Unable to kill {0}".format(name))
        return
# class KillAll
