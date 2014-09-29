Broadcaster
===========

A broadcaster implements a one-to-many pipe.



.. uml::

   BaseClass <|-- Broadcaster

.. module:: apetools.commons.broadcaster
.. autosummary::
   :toctree: api

   Broadcaster
   Broadcaster.receivers
   Broadcaster.temp_receivers
   Broadcaster.subscribe
   Broadcaster.unsubscribe
   Broadcaster.set_up
   Broadcaster.reset
   Broadcaster.__contains__
   Broadcaster.__iter__
   Broadcaster.__call__

