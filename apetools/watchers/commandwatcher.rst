Command Watcher
===============

A module to repeatedly call a bash command and log its output.



.. uml::

   BaseThreadClass <|-- CommandWatcher

.. module:: apetools.watchers.commandwatcher
.. autosummary::
   :toctree: api

   CommandWatcher
   CommandWatcher.expression
   CommandWatcher.timestamp
   CommandWatcher.stop
   CommandWatcher.__call__
   CommandWatcher.start
   CommandWatcher.run

