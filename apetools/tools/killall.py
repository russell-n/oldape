
#python
import re

# apetools
from apetools.baseclass import BaseClass
from apetools.tools import sleep
from apetools.commons import enumerations, expressions, errors
from apetools.parsers.oatbran import NAMED, STRING_START,SPACES, INTEGER
from apetools.commands.pscommand import PsGrep
from apetools.commands.topcommand import TopGrep


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
    def __init__(self, connection=None, name=None, time_to_sleep=0, level=None):
        """
        :param:

         - `name`: The name of a process to kill
         - `time_to_sleep`: The number of seconds to wait for a process to die.
         - `connection`: A connection to a device
         - `level`: the signal level (as a positive integer)
        """
        super(BaseClass, self).__init__()
        self._logger = None
        self.name = name
        self._arguments = None
        self.time_to_sleep = time_to_sleep
        self._sleep = None
        self._connection = None
        self.connection = connection
        self._grep = None
        self._level = None
        self.level = level
        return

    @property
    def level(self):
        """
        The signal level for ``kill``
        """
        if self._level is None:
            self._level = ''
        return self._level

    @level.setter
    def level(self, level):
        """
        Set the signal level (use None to reset it to the default)

        :param:

         - `level`: positive integer or None
        """
        if level is not None:
            self._level = "-{0}".format(level)
        else:
            self._level = level
        return

    @property
    def connection(self):
        """
        A connection to the device
        """
        return self._connection

    @connection.setter
    def connection(self, connection):
        """
        Sets the connection, resets the grep (since the OS may have changed)

        :param:

         - `connection` : a connection to the device (e.g. `SSHConnection`)

        :postcondition: self._grep is None, self._connection is `connection`
        """
        self._connection = connection
        self._grep = None
        return

    @property
    def grep(self):
        """
        the parser for the process id's
        """
        if self._grep is None:
            if self.connection.operating_system == operating_systems.ios:
                self._grep = TopGrep(self.connection)
            else:
                self._grep = PsGrep(self.connection)
        return self._grep


    @property
    def sleep(self):
        """
        A sleep object to pace the execution of commands on the device
        
        :return: A sleep timer
        """
        if self._sleep is None:
            self._sleep = sleep.Sleep(self.time_to_sleep).run
        return self._sleep

    def kill(self, name, level=None):
        """
        Tries to kill all matching processes

        :param:

         - `name`: the name of the process
         - `level`: a signal level to override the set level
        """
        if level is None:
            level = self.level
        kill_count = 0
                
        for pid in self.grep(name):
            self.logger.debug("killing: " + pid)
            command = " {0} {1}".format(self.level, pid)
            kill_count+= 1
            self.logger.debug("kill " + command)
            k_output, k_error = self.connection.kill(command)
            for k_line in k_error:
                if len(k_line) > 1:
                    self.logger.error(k_line)
        return kill_count
    
    def run(self, name=None, time_to_sleep=None):
        """
        Executes the kill
        
        :param:

         - `name`: The process to kill
         - `time_to_sleep`: Seconds between calls to the device

        :raise: KillAllError if the process is still alive at the end
        """
        if name is None:
            name = self.name
        
        if time_to_sleep is None:
            time_to_sleep = self.time_to_sleep

        self.logger.debug("process to kill: {0}".format(name))

        kill_count = self.kill(name)
        
        if not kill_count:
            self.logger.info("No iperf sessions found on {0}".format(self.connection.hostname))
            return

        self.sleep(time_to_sleep)

        # double-check to see if the process is dead
        for pid in self.grep(name):
            raise KillAllError("Unable to kill {0}".format(name))
            self.logger.error(err)
        self.logger.info("Killed {0} iperf processes on {1}".format(kill_count, self.connection.hostname))
        return

    def __call__(self, name=None, time_to_sleep=None):
        """
        This is an alias to ``run`` to match the newer-style

        :param:

         - `name`: The process to kill
         - `time_to_sleep`: Seconds between calls to the device

        :raise: KillAllError if the process is still alive at the end
        """
        self.run(name=name, time_to_sleep=time_to_sleep)
        return
    
    def __str__(self):
        return "{0} ({2}):{1}".format(self.__class__.__name__, self.name, self.connection)
# end class KillAll


#python standard library
import unittest
from random import randrange, choice
#third-party
from mock import MagicMock, patch, call
from nose.tools import raises


class TestKillAll(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.kill = KillAll(connection=self.connection)
        return
    
    def test_set_connection(self):
        """
        Does setting the connection re-set the grep?
        """
        self.connection.operating_system = operating_systems.ios
        self.assertIsInstance(self.kill.grep, TopGrep)
        self.connection.operating_system = operating_systems.android
        self.kill.connection = self.connection
        self.assertIsInstance(self.kill.grep, PsGrep)
        return

    def test_kill_command(self):
        """
        Will the correct kill command be called?
        """
        pgrep = MagicMock()
        self.connection.operating_system = operating_systems.linux
        self.connection.kill.return_value = [""], [""]
        # pids[0] is the first traversal over pids , pids[1] is the check for unkilled pids
        pids = [['{0}'.format(randrange(1000)) for i in range(randrange(100))]] + [[]]
        def side_effects(*args, **kwargs):
            return pids.pop(0)
        pgrep.side_effect = side_effects
        expected = [call("  {0}".format(pid)) for pid in pids[0]]

        self.kill._grep = pgrep
        self.kill.run(name='emacs',
                    time_to_sleep=0)
        self.assertEqual(self.connection.kill.call_args_list, expected)
        return

    @raises(KillAllError)
    def test_failed_kill(self):
        """
        Will a failed kill raise an error?
        """
        pgrep = MagicMock()
        self.connection.operating_system = operating_systems.linux
        self.connection.kill.return_value = [""], [""]

        pids = ['{0}'.format(randrange(1000)) for i in range(randrange(100))]
        pgrep.return_value = pids

        self.kill._grep = pgrep
        self.kill.run(name='emacs',
                    time_to_sleep=0)
        return

    def test_call(self):
        """
        Dose `__call__` do the same thing as `run`?
        """
        pgrep = MagicMock()
        self.connection.operating_system = operating_systems.linux
        self.connection.kill.return_value = [""], [""]

        # pids[0] is the first traversal over pids , pids[1] is the check for unkilled pids
        pids = [['{0}'.format(randrange(1000)) for i in range(randrange(100))]] + [[]]
        def side_effects(*args, **kwargs):
            return pids.pop(0)
        pgrep.side_effect = side_effects

        # use the default kill level
        self.kill.level = None
        expected = [call("  {0}".format(pid)) for pid in pids[0]]

        self.kill._grep = pgrep
        self.kill(name='emacs',
                  time_to_sleep=0)
        self.assertEqual(self.connection.kill.call_args_list, expected)
        return

    def test_set_level(self):
        """
        If you set the level, will the command change?
        """
        pgrep = MagicMock()
        self.connection.kill.return_value = [""], [""]
        level = randrange(100)
        self.kill.level = level
        self.assertEqual(self.kill.level, "-{0}".format(level))
        # pids[0] is the first traversal over pids , pids[1] is the check for unkilled pids
        pids = [['{0}'.format(randrange(1000)) for i in range(randrange(100))]] + [[]]
        def side_effects(*args, **kwargs):
            return pids.pop(0)
        pgrep.side_effect = side_effects
        expected = [call(" -{1} {0}".format(pid, level)) for pid in pids[0]]

        self.kill._grep = pgrep
        self.kill.kill(name='emacs')
        self.assertEqual(self.connection.kill.call_args_list, expected)
        return

    def test_reset_level(self):
        """
        Can you go back to the default level?
        """
        pgrep = MagicMock()
        self.connection.kill.return_value = [""], [""]
        level = randrange(100)
        self.kill.level = level
        # reset here
        self.kill.level = None
        self.assertEqual(self.kill.level, "")
        # pids[0] is the first traversal over pids , pids[1] is the check for unkilled pids
        pids = [['{0}'.format(randrange(1000)) for i in range(randrange(100))]] + [[]]
        def side_effects(*args, **kwargs):
            return pids.pop(0)
        pgrep.side_effect = side_effects
        expected = [call("  {0}".format(pid)) for pid in pids[0]]

        self.kill._grep = pgrep
        self.kill.kill(name='emacs')
        self.assertEqual(self.connection.kill.call_args_list, expected)
        return

        
