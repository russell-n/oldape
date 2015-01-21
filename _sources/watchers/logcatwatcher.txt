Logcat Watcher
==============

A module for watchers of logcat logs.



.. uml::

   LogWatcher <|-- LogcatWatcher

.. module:: apetools.watchers.logcatwatcher
.. autosummary::
   :toctree: api

   LogcatWatcher
   LogcatWatcher.logs
   LogcatWatcher.arguments
   LogcatWatcher.execute
   LogcatWatcher.__str__

::

    if __name__ == "__main__":
        import sys
        lw = LogcatWatcher(sys.stdout)
        print lw.arguments
        lw.run()
    
    

