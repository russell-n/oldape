
#python Libraries
from StringIO import StringIO
import Queue
import threading
from abc import ABCMeta, abstractmethod

# apetools Libraries
from apetools.baseclass import BaseThreadClass
from localconnection import OutputError 
from apetools.commons import enumerations


SPACER = '{0} {1} '
UNKNOWN = "Unknown command: "
EOF = ''


class NonLocalConnection(BaseThreadClass):
    """
    A non-local connection is the base for non-local connections

    """
    __metaclass__ = ABCMeta
    def __init__(self, command_prefix='', lock=None, 
                 operating_system=enumerations.OperatingSystem.linux,
                 path=None, library_path=None, identifier=None,
                 *args, **kwargs):
        """
        NonLocalConnection Constructor
        
        :param:

         - `command_prefix`: A prefix to prepend to commands (e.g. 'adb shell')
         - `lock` : A lock to acquire before calls
         - `operating_system`: the operating system
         - `path`: a path setting to add to the path (before :$PATH)
         - `library_path`: a setting for LD_LIBRARY_PATH
         - `identifier`: string to use to identify the connection
        """
        super(NonLocalConnection, self).__init__(*args, **kwargs)
        # logger is defined in BaseClass but declared here for child-classes
        self._logger = None
        self.command_prefix = command_prefix
        self._lock = lock
        self.path = path
        self.library_path = library_path
        self.identifier = identifier
        self._queue = None
        self.operating_system = operating_system
        self.exc_info = None
        return

    @property
    def lock(self):
        """
        :return: a re-entrant lock
        """
        if self._lock is None:
            self._lock = threading.RLock()
        return self._lock
    
    @property
    def queue(self):
        """
        :rtype: Queue.Queue
        :return: the local Queue
        """
        if self._queue is None:
            self._queue = Queue.Queue()
        return self._queue

    def add_path(self, command):        
        """
        Prepends any path additions passed in at instantiation to the command

        :param:
        
         - `command`: the name of a command
        :return: command with path additions if given
        """
        if self.path is not None:
            command = "PATH={0}:$PATH;{1}".format(self.path, command)
        if self.library_path is not None:
            command = "export LD_LIBRARY_PATH={0}:$LD_LIBRARY_PATH;{1}".format(self.library_path,
                                                                        command)
        return command

    def _procedure_call(self, command, arguments='', timeout=None):
        """
        This is provided so it can be overriden by subclasses.
        It is what's called directly by __getattr__ to support LocalConnection.command() calls

        Otherwise it just returns _main()
        """
        command = self.add_path(command)
        return self._main(command, arguments, timeout)
    
    def _main(self, command, arguments='', timeout=None):
        """
        :param:

         - `command`: the command string to execute
         - `arguments`: The arguments for the command
         - `timeout`: A timeout for the queue when doing a get

        :return: OutputError named tuple
        """
        self.logger.debug("command: '{0}', arguments: '{1}', timeout: '{2}'".format(command,
                                                                                    arguments,
                                                                                    timeout))
        thread = self.start(command, arguments)
        try:
            if self.exc_info:
                raise self.exc_info[1], None, self.exc_info[2]
            return self.queue.get(timeout=timeout)
        except Queue.Empty as error:
            self.logger.debug(error)
            if thread is not None:
                del(thread)
        return OutputError(StringIO(''),StringIO( "'{0} {1}' timed out".format(command, arguments)))

    def run(self, command, arguments):
        """
        Runs the command in a thread and puts the output and error on the queue

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.

        :postcondition: OutputError with output and error file-like objects
        :raise: NotImplementedError if sub-class doesn't override this method
        """
        raise(NotImplementedError("Sub-classes need to implement the run"))
        return

    def start(self, command, arguments):
        """
        starts run in a thread

        :return: the thread object
        """
        t = threading.Thread(target=self.run_thread, args=((command,arguments)),
                             name=self.__class__.__name__)
        t.daemon = True
        t.start()
        self.logger.debug(",".join([t.name for t in threading.enumerate() if t.name != "MainThread"]))
        return t

    def __getattr__(self, command):
        """
        The parameters are the same as _procedure_call()
        
        :param:

         - `command`: The command to call.

        :return: _procedure_call method called with passed-in args and kwargs
        """
        def procedure_call(*args, **kwargs):
            return self._procedure_call(command, *args, **kwargs)
        return procedure_call

    def __call__(self, command, arguments='', timeout=None):
        """
        A pass-through to the _main method to use when the dot-notation doesn't work

        :param:

         - `command`: the command string to execute
         - `arguments`: The arguments for the command
         - `timeout`: A timeout for the queue when doing a get

        :return: OutputError named tuple
        """
        return self._procedure_call(command=command, 
                                    arguments=arguments, timeout=timeout)        

    def __str__(self):
        return "{0}".format(self.__class__.__name__)
# end class NonLocalConnection


class DummyConnection(NonLocalConnection):
    """
    A dummy connection is used to fake connections in commands.
    """
    def __init__(self, *args, **kwargs):
        super(DummyConnection, self).__init__(*args, **kwargs)
        self.main_string = "command={0}, arguments={1}, timeout={2}"
        self.run_string = "command={0}, arguments={1}"
        self.hostname = 'DummyConnection'
        return

    def _main(self, command, arguments, timeout):
        """
        Does nothing.

        :return: OutputError with EOF in both
        """
        self.logger.debug(self.main_string.format(command,
                                                 arguments,
                                                 timeout))
        return OutputError(StringIO(''), StringIO(''))


# python standard library
import unittest
import random
import string
#third party
from mock import MagicMock


class TestDummyConnection(unittest.TestCase):
    def setUp(self):
        self.dummy = DummyConnection()
        self.dummy._logger = MagicMock()
        self.source_string = string.letters+ string.digits+ string.punctuation
        return

    def random_input(self):
        """
        :return: random string
        """
        return "".join(random.sample(self.source_string,
                                          len(self.source_string)))
        
    def test_call(self):
        """
        Can you call it and get no output or errors?
        """
        command = self.random_input()
        arguments = self.random_input()
        o,e = self.dummy(command, arguments)
        self.dummy.logger.debug.assert_called_with(self.dummy.main_string.format(command,
                                                           arguments,
                                                           None))
        for index,line in enumerate(o):
            self.assertEqual(index, 0)
        for index, line in enumerate(e):
            self.assertEqual(index, 0)
        return

    def test_dot_notation(self):
        """
        Does the dot-notation work?
        """
        arguments = self.random_input()
        o, e = self.dummy.ummagumma(arguments)
        self.dummy.logger.debug.assert_called_with(self.dummy.main_string.format('ummagumma',
                                                                                 arguments,
                                                                                 None))
        return
