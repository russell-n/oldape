Log Watcher Builder
===================

A module to build logwatchers.



.. uml::

   ConfigurationError <|-- LogWatcherBuilderError

.. module:: apetools.builders.subbuilders.logwatcherbuilders
.. autosummary::
   :toctree: api

   LogwatcherBuilderError



.. uml::

   BaseClass <|-- BaseWatcherBuilder

.. autosummary::
   :toctree: api

   BaseWatcherBuilder
   BaseWatcherBuilder.arguments
   BaseWatcherBuilder.output_file



.. uml::
   
   BaseWatcherBuilder <|-- LogcatWatcherBuilder
   LogcatWatcherBuilder o- LogcatWatcher

.. autosummary::
   :toctree: api

   LogcatWatcherBuilder
   LogcatWatcherBuilder.arguments
   LogcatWatcherBuilder.buffers
   LogcatWatcherBuilder.product

    
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


.. uml::

   BaseWatcherBuilder <|-- LogWatcherBuilder
   LogWatcherBuilder o- LogWatcher

.. autosummary::
   :toctree: api

   LogWatcherBuilder
   LogWatcherBuilder.product



.. uml::

   BaseWatcherBuilder <|-- PingWatcherBuilder
   PingWatcherBuilder o- PingWatcher

.. autosummary::
   :toctree: api

   PingWatcherBuilder
   PingWatcherBuilder.arguments
   PingWatcherBuilder.target
   PingWatcherBuilder.threshold
   PingWatcherBuilder.product



.. uml::

   BaseWatcherBuilder <|-- LogFollowerBuilder
   LogFollowerBuilder o- LogFollower

.. autosummary::
   :toctree: api

   LogFollowerBuilder
   LogFollowerBuilder.product

    
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
