"""
A module to build logwatchers
"""

from apetools.baseclass import BaseClass
from apetools.commons.errors import ConfigurationError

from apetools.watchers.logcatwatcher import LogcatWatcher
from apetools.watchers.logwatcher import LogWatcher
from apetools.watchers.logfollower import LogFollower
from apetools.watchers.pingwatcher import PingWatcher

class LogwatcherBuilderError(ConfigurationError):
    """
    """
# end LogWatcherBuilerError

APPEND = 'a'

class BaseWatcherBuilder(BaseClass):
    """
    A class to base other builders on
    """
    def __init__(self, node, parameters, output,
                 name=None, event=None):
        """
        :param:

         - `node`: device to watch        
         - `parameters`: named tuple built from config file
         - `output`: storageobject to send output to
         - `name`: a name to add to the output file
         - `event`: event to watch to decide when to stop
        """
        super(BaseWatcherBuilder, self).__init__()
        self._logger = None
        self.node = node
        self.parameters = parameters
        self.event = event
        self.name = name
        self.output = output
        self._product = None
        self._output_file = None
        self._arguments = None
        return

    @property
    def arguments(self):
        """
        :return: arguments to the command
        """
        if self._arguments is None:
            try:
                self._arguments = self.parameters.arguments
            except AttributeError as error:
                self.logger.error(error)
                raise LogwatcherBuilderError("Missing arguments parameter")
        return self._arguments

    @property
    def output_file(self):
        """
        :return: opened file to send output to
        """
        if self._output_file is None:
            if '/' in self.arguments:
                arguments = self.arguments.split('/')[-1]
            else:
                arguments = self.arguments
            prefix = "{0}_{1}".format(self.parameters.type,
                                      arguments)
            if self.name is not None:
                prefix = "{0}_{1}".format(prefix, self.name)

            self._output_file = self.output.open("{0}.log".format(prefix),
                                                 subdir="logs",
                                                 mode=APPEND)
        return self._output_file

# end class BaseWatcherBuilder

    
class LogcatWatcherBuilder(BaseWatcherBuilder):
    """
    A builder of logcat watchers
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `node`: device to watch        
         - `parameters`: named tuple built from config file
         - `output`: storageobject to send output to
         - `name`: a name to add to the output file
         - `event`: event to watch to decide when to stop
        """
        super(LogcatWatcherBuilder, self).__init__(*args, **kwargs)
        self._buffers = None
        return

    @property
    def arguments(self):
        """
        :return: string of buffers       
        """
        if self._arguments is None:
            if self.buffers is None:
                self._arguments = "all"
            else:
                self._arguments = "_".join(self.buffers)
        return self._arguments

    @property
    def buffers(self):
        """
        :return: buffers list or None        
        """
        if self._buffers is None:
            buffers = self.parameters.buffers
            if buffers == "all":
                buffers = None
            if buffers is not None:
                buffers = buffers.split(',')         
        return self._buffers
    
    @property
    def product(self):
        """
        :return: logcatwatcher
        """
        if self._product is None:
            self._product = LogcatWatcher(output=self.output_file,
                                          connection=self.node.connection,
                                          logs=self.buffers)
        return self._product
    
# end class LogcatWatcherBuilder

class LogWatcherBuilder(BaseWatcherBuilder):
    """
    A builder of log watchers
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `node`: device to watch        
         - `parameters`: named tuple built from config file
         - `output`: storageobject to send output to
         - `name`: a name to add to the output file
         - `event`: event to watch to decide when to stop
        """
        super(LogWatcherBuilder, self).__init__(*args, **kwargs)
        self._arguments = None
        return

    @property
    def product(self):
        """
        :return: logcatwatcher
        """
        if self._product is None:
            self._product = LogWatcher(output=self.output_file,
                                       connection=self.node.connection,
                                       arguments=self.arguments)
        return self._product
    
# end class LogcatWatcherBuilder
class PingWatcherBuilder(BaseWatcherBuilder):
    """
    A builder of ping watchers
    """
    def __init__(self, *args, **kwargs):
        """
        PingWatcherBuilder Constructor

        :param:

         - `node`: device to watch        
         - `parameters`: named tuple built from config file
         - `output`: storageobject to send output to
         - `name`: a name to add to the output file
         - `event`: event to watch to decide when to stop
        """
        super(PingWatcherBuilder, self).__init__(*args, **kwargs)
        self._target = None
        self._threshold = None
        return

    @property
    def arguments(self):
        return self.target
    
    @property
    def target(self):
        """
        Hostname to ping
        """
        if self._target is None:
            self._target = self.parameters.target
        return self._target

    @property
    def threshold(self):
        """
        Consecutive failed pings to consider a failure
        """
        if self._threshold is None:
            if hasattr(self.parameters, 'threshold'):
                self._threshold = int(self.parameters.threshold)
            else:
                self._threshold = 5
        return self._threshold
    
    @property
    def product(self):
        """
        :return: logcatwatcher
        """
        if self._product is None:
            self._product = PingWatcher(target=self.target,
                                        threshold=self.threshold,
                                        output=self.output_file,
                                        connection=self.node.connection)
        return self._product
    
# end class PingWatcherBuilder
    
class LogFollowerBuilder(BaseWatcherBuilder):
    """
    A builder of log followers
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `node`: device to watch        
         - `parameters`: named tuple built from config file
         - `output`: storageobject to send output to
         - `name`: a name to add to the output file
         - `event`: event to watch to decide when to stop
        """
        super(LogFollowerBuilder, self).__init__(*args, **kwargs)
        self._arguments = None
        return

    @property
    def product(self):
        """
        :return: log-follower
        """
        if self._product is None:
            self._product = LogFollower(output=self.output_file,
                                        connection=self.node.connection,
                                        arguments=self.arguments)
        return self._product
    
# end class LogcatWatcherBuilder
    
