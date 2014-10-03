Log Watcher
===========

A module for watchers of kmsg logs.



LogWatcherError
---------------

.. uml::

   CommandError <|-- LogWatcherError

.. module:: apetools.watchers.logwatcher
.. autosummary::
   :toctree: api

   LogWatcherError



Log Watcher
-----------

.. uml::

   BaseThreadClass <|-- LogWatcher

.. autosummary::
   :toctree: api

   LogWatcher
   LogWatcher.timestamp
   LogWatcher.stop
   LogWatcher.stopped
   LogWatcher.execute
   LogWatcher.run
   LogWatcher.start



Safe Log Watcher
----------------

.. uml::

   LogWatcher <|-- SafeLogWatcher

.. autosummary::
   :toctree: api

   SafeLogWatcher
   SafeLogWatcher.run

::

    if __name__ == "__main__":
        import sys
        kw = LogWatcher(sys.stdout)
        print kw.arguments
        kw.run()
    
    

