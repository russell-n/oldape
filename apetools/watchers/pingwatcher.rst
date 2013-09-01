The Ping Watcher
================
.. currentmodule:: apetools.watchers.pingwatcher

The Ping Watcher is a change-in-connectivity monitor for network connections.



.. uml::

   FailureData -|> namedtuple
   FailureData : timestamp
   FailureData : elapsed

.. autosummary::
   :toctree: api

   FailureData
   FailureData.__str__
   


.. uml::
   
   RecoveryData -|> FailureData

.. autosummary::
   :toctree: api

   RecoveryData



.. uml::

   PingWatcherError -|> CommandError

.. autosummary::
   :toctree: api

   PingWatcherError

<<name='PingWatcherError', echo=False>>
class PingWatcherError(CommandError):
    """
    An error to raise if something is wrong with the PingWatcher
    """
# end class PingWatcherError


.. uml::

   PingWatcher -|> BaseThreadClass

.. autosummary::
   :toctree: api

   PingWatcher
   PingWatcher.arguments
   PingWatcher.expression
   PingWatcher.run
   


