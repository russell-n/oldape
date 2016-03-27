
# python standard library
from abc import ABCMeta, abstractmethod, abstractproperty
from threading import Thread

#apetools
from apetools.baseclass import BaseThreadClass, BaseClass
from apetools.commons.errors import CommandError

class BaseThreadedCommand(BaseThreadClass):
    """
    An abstract base-class for simple commands to run in a thread
    """
    __metaclass__ = ABCMeta
    def __init__(self):
        """
        Only instantiates the BaseClass and sets the properties
        """
        super(BaseThreadedCommand, self).__init__()
        self._logger = None
        self.stopped = False
        self._thread = None
        return

    @abstractmethod
    def run(self):
        """
        The method put into the thread.
        """
        return

    @abstractmethod
    def stop(self):
        """
        :postcondition: the thread is stopped 
        """
        return
    
    def __call__(self, *args, **kwargs):
        """
        The main interface for the command.

        Calls run and puts it in a daemonized thread.

        :postcondition: self.thread is a running thread
        """
        #import pudb;pudb.set_trace()
        self.thread = Thread(target=self.run_thread, args=args,
                             kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()
        return

    def __del__(self):
        """
        :postcondition: `stop` is called.
        :postcondition: connection is closed
        """
        self.stop()
        return
# end class BaseThreadedCommand

class ProcessCommandEnum(object):
    __slots__ = ()
    missing = 'missing'
    bad_arg = 'bad_arg'

class ProcessGrepEnum(object):
    __slots__ = ()
    pid = 'pid'
    process = 'process'

class BaseProcessCommand(BaseClass):
    """
    A parent class for process-commands (e.g. ``ps``)
    """
    __metaclass__ = ABCMeta
    def __init__(self, connection=None):
        """
        BaseProcessCommand Constructor

        :param:

         - `connection`: Connection to a device
        """
        super(BaseProcessCommand, self).__init__()
        self._logger = None
        self._connection = None
        self.connection = connection
        self._arguments = None
        self._error_expression = None
        self._error_messages = None
        self._command = None
        return

    @property
    def connection(self):
        """
        The connection to the device

        :return: the device connection
        """
        return self._connection

    @connection.setter
    def connection(self, connection):
        """
        Sets the connection and re-sets the arguments

        :param:

         - `connection`: a connection to a device

        :postcondition: self.arguments is None and self.connection set to connection
        """
        self._connection = connection
        self._arguments = None
        return
    
    @abstractproperty
    def arguments(self):
        """
        the arguments for the command based on the operating system
        """
        return

    @abstractproperty
    def command(self):
        """
        The actual command that's issued (used for logging and ID)
        """
        return self._command    

    @property
    def error_messages(self):
        """
        A dictionary of error-messages

        :return: error messages for the `check_errors`
        """
        if self._error_messages is None:
            self._error_messages = {ProcessCommandEnum.missing:"the `{0}` command wasn't found (is it installed?)".format(self.command),
                                    ProcessCommandEnum.bad_arg:"Unrecognized argument `{0}`".format(self.arguments)}    
        return self._error_messages


    @abstractproperty
    def error_expression(self):
        """
        Holds the expression to match error messages

        :return: compiled regular expression to match error messages
        """
        return

    @abstractmethod
    def run(self):
        """
        This is where the connection is called. Since it changes with each command it is separated out
        """
        return

    def __call__(self):
        """
        Calls the process command and generates the output

        :yield: Stdout for the process command
        """
        self.logger.debug("Calling: {0}".format(self))
        output, error = self.run()

        for index, line in enumerate(output):
            self.logger.debug(line)
            yield line

        if index == 0:
            self.logger.warning("No processes found, check `{0}`".format(self))
        for line in error:
            self.check_errors(line)
        return

    def check_errors(self, line):
        """
        Check the line for known errors

        :param:

         - `line`: a line with possible top-related errors

        :raise: `CommandError` if an error is detected
        """
        match = self.error_expression.search(line)
        if match:
            self.logger.error(line)
            error_map = match.groupdict()
            for key, value in error_map.iteritems():
                if value is not None:
                    raise CommandError(self.error_messages[key])
        return

    def __str__(self):
        """
        The command issued over the connection

        :return: command and arguments
        """
        return "{0} {1}".format(self.command, self.arguments)
# end class BaseProcessCommand

class BaseProcessGrep(BaseClass):
    """
    A base class to grep process information
    """
    __metaclass__ = ABCMeta
    def __init__(self, connection, process=None, field=ProcessGrepEnum.pid):
        """
        BaseProcessGrep Constructor

        :param:

         - `connection`: connection to a device
         - `process`: The name of the process to get (if not set pass into call())
         - `field`: Column to extract from the command output (e.g. pid)
        """
        super(BaseProcessGrep, self).__init__()
        self._logger = None
        self._connection = None
        self.connection = connection
        self._expression = None
        self.process = process
        self._process_query = None
        self.field = field      
        return

    @abstractproperty
    def expression(self):
        """
        The compiled regular expression to match the process output
        """        
        return
    
    @abstractproperty
    def process_query(self):
        """
        The command to query the device for process information        
        """
        return

    @property
    def connection(self):
        """
        The connection to the device
        """
        return self._connection

    @connection.setter
    def connection(self, connection):
        """
        Sets the connection for the process_query

         * self.process_query is reset to None as there is a circular reference
         to the connection if you try to set it directly

        :param:

         - `connection`: Connection to the device

        :postcondition: self.process_query and self.expression set to None
        """
        self.logger.debug("Setting the connection and unsetting expression and process_query")
        self._connection = connection
        self._expression = None
        self._process_query = None
        return

    def __call__(self, process=None):
        """
        Finds the process name and generates PIDs

         * If a process name is passed in, self.process is set to it

        :param:

         - `process`: the name of a process

        :yield: PID for process
        """
        if process is not None:
            self._expression = None
            self.process = process
        for line in self.process_query():
            match = self.expression.search(line)
            if match:
                line_map = match.groupdict()
                yield line_map[self.field]
        return