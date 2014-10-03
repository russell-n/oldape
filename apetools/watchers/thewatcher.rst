The Watcher
===========

The Watcher watches Watchers.



The Watcher Error
-----------------

.. uml::

   CommandError <|-- TheWatcherError

.. module:: apetools.watchers.thewatcher
.. autosummary::
   :toctree: api

   TheWatcherError



The Watcher
-----------

.. uml::

   BaseClass <|-- TheWatcher

.. autosummary::
   :toctree: api

   TheWatcher
   TheWatcher.start
   TheWatcher.stop
   TheWatcher.__call__
   TheWatcher.__del__

