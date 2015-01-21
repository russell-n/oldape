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

